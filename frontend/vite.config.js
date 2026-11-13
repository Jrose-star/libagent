import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path' // 1. 引入 path 模块

export default defineConfig({
  plugins: [vue()],
  resolve: {
    // 2. 添加 resolve 配置
    alias: {
      // 3. 定义 @router 指向 src/router 文件夹的绝对路径
      '@router': path.resolve(__dirname, 'src/router'),
      // 通常还会定义一个 @ 符号指向 src 目录，这在项目中非常常用
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    proxy: {
      // API 接口代理
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      // 静态文件代理（头像图片）
      '/uploads': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})
