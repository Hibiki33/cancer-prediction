/// <reference types="vite/client" />
declare module 'spark-md5';

declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}
