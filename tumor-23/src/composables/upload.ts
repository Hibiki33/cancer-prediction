import SparkMD5 from 'spark-md5'
import axios from '~/api/axio'
let fileHash:any
let fileName:any

export const handleUpload = async (file: any, fileList: any) => {
    console.log('开始上传文件')
    if (!file) {
        return
    }
    console.log(file)
    console.log(typeof file)
    let fileName = file.name
    console.log(fileName)
    let fileChunkList = createFileChunks(file.raw)
    const hashPromise = calculateHash(fileChunkList);
    await hashPromise
    hashPromise.then(
        hash => {
            console.log(hash)
            fileHash = hash
            uploadChunks(fileChunkList).then(r => {})
        }
    )
}

const CHUNK_SIZE = 1024 * 1024

const createFileChunks = (file: File) => {
    const fileChunkList = []
    let cur = 0
    while (cur < file.size) {
        fileChunkList.push({
            file: file.slice(cur, cur + CHUNK_SIZE)
        })
        cur += CHUNK_SIZE
    }
    return fileChunkList
}

const calculateHash = async (fileChunks: Array<{file: Blob}>) => {
    return new Promise(resolve => {
        const spark = new SparkMD5.ArrayBuffer()
        const chunks: Blob[] = []
        fileChunks.forEach((chunk, index) => {
            if (index === 0 || index === fileChunks.length - 1) {
                chunks.push(chunk.file)
            } else {
                chunks.push(chunk.file.slice(0, 2))
                chunks.push(chunk.file.slice(CHUNK_SIZE / 2, CHUNK_SIZE / 2 + 2))
                chunks.push(chunk.file.slice(CHUNK_SIZE - 2, CHUNK_SIZE))
            }
        })
        const reader = new FileReader()
        reader.readAsArrayBuffer(new Blob(chunks))
        reader.onload = (e:Event) => {
            spark.append((<FileReader>e?.target)?.result as ArrayBuffer)
            resolve(spark.end())
        }
    })
}

const uploadChunks = async (fileChunks: Array<{file: Blob}>) => {
    const data = fileChunks.map(({ file }, index) => ({
        fileHash: fileHash,
        index,
        chunkHash: `${fileHash}-${index}`,
        chunk: file,
        size: file.size,
    }))

    const formDatas = data.map(({ chunk, chunkHash }) => {
        const formData = new FormData()
        formData.append('chunk', chunk)
        formData.append('chunkHash', chunkHash)
        formData.append('fileName', fileName)
        formData.append('fileHash', fileHash)
        return formData
    })

    let index = 0
    const max = 6
    const taskPool: any = []

    while (index < formDatas.length) {
        const task = axios.post('fileManager/uploadc/', formDatas[index])

        task.then(() => {
            taskPool.splice(taskPool.findIndex((item: any) => item === task))
        })
        taskPool.push(task);
        if (taskPool.length === max) {
            // 当请求队列中的请求数达到最大并行请求数的时候，得等之前的请求完成再循环下一个
            await Promise.race(taskPool)
        }
        index++
        // percentage.value = (index / formDatas.length * 100).toFixed(0)
    }

    const formData = new FormData();
    formData.append('fileHash', fileHash);
    formData.append('fileName', fileName);

    await Promise.all(taskPool).then(() => {    // 发送 merge 请求
        axios.post('fileManager/merge/', formData)
    })

}
