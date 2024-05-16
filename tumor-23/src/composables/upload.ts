import SparkMD5 from 'spark-md5'
import axios from '~/api/axio'

let fileHash:any
let fileName:any
let preview: any
export const handleUpload = async (file: any, fileList: any) => {
    // const formData = new FormData();
    // formData.append('fileHash', "5012b46e6560a5e49a0da4353b6c0a1c");
    // formData.append('fileName', "5012b46e6560a5e49a0da4353b6c0a1c.svs");
    // console.log("merge!")
    // axios.post('fileManager/merge/', formData).then(response => {
    //     const data = response.data
    //     console.log(data)
    //     preview = data.preview
    // })
    //
    // return preview;
    console.log('开始上传文件')
    console.log(typeof file.raw)


    if (!file) {
        return
    }

    fileName = file.name
    console.log("filename: " + fileName);
    let fileChunkList = createFileChunks(file.raw)
    // const hashPromise = calculateHash(fileChunkList);
    //
    // await hashPromise
    //
    // hashPromise.then(
    //     hash => {
    //         fileHash = hash
    //         // uploadChunks(fileChunkList)
    //     }
    // )

    await sleep(1000)
    fileHash = await calculateHash(fileChunkList);
    console.log("hash: " + fileHash);
    console.log("name: " + fileName);
    const reader = new FileReader();
    reader.readAsText(file.raw);
    reader.onload = () => {
        const formData = new FormData();
        formData.append('fileName', fileName);
        formData.append('fileHash', fileHash);
        formData.append('chunkHash', fileHash);
        // formData.append("chunk", reader.result.toString());

        axios.post('fileManager/uploadc/', formData);
    }


    return preview
}

function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
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

async function readFileData(file: any): Promise<string | ArrayBuffer | null> {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            resolve(reader.result);
        };
        reader.onerror = () => {
            reject(reader.error);
        };
        reader.readAsDataURL(file);
    });
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
    let index = 0;

    index = 0
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
        sleep(1000)
        axios.post('fileManager/merge/', formData)
            .then(response => {
            const data = response.data
            console.log(data)
            preview = data.preview
        })
    })

}
