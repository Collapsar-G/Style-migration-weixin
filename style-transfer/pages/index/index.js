// index.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    elements: [{
      title: '布局',
      name: 'layout',
      color: 'red',
      icon: 'newsfill'
    },
    {
      title: '布局',
      name: 'layout',
      color: 'pink',
      icon: 'newsfill'
    }
    ],
    src:"../../icon/btn.png"
  },

  onLoad() {

  },
  changePic(){
    this.setData({
      src:"../../icon/btn2.png"
    })
  },
  changePicBack(){
    this.setData({
      src:"../../icon/btn.png"
    })
  }
})
