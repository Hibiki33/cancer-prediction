import { createApp } from "vue";
import App from "./App.vue";
import { store, key } from './store/store'
import Diagnose from "./Diagnose.vue";


// import "~/styles/element/index.scss";

// import ElementPlus from "element-plus";
// import all element css, uncommented next line
// import "element-plus/dist/index.css";

// or use cdn, uncomment cdn link in `index.html`

import "~/styles/index.scss";
import "uno.css";

// If you want to use ElMessage, import it.
import "element-plus/theme-chalk/src/message.scss";
import router from "./router";
import VueCropper from 'vue-cropper';
import 'vue-cropper/dist/index.css'
import axios from "~/api/axio";

const app = createApp(App);
// app.use(ElementPlus);
app.use(router);
app.use(store, key)
app.use(VueCropper)
app.mount("#app");



