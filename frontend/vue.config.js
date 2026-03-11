module.exports = {
  devServer: {
    proxy: {
      '/auth': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/admin': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/company': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/student': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
}
