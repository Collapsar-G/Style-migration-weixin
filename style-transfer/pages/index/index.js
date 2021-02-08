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
    src:"../../icon/btn.png",
    animationData:{},
    hidden:false,
    TheOpacity: 1
  },
  onLoad() {

  },
  bindChange:function(e){
    let that = this
    var animation = wx.createAnimation({
      duration: 300,
      timingFunction: 'linear',
    })

    this.animation = animation
 
    animation.opacity(0.5).step()
 
    this.setData({
      animationData: animation.export()
    })
 
    setTimeout(function () {
      wx.navigateTo({
        url: '../create/create'
      })
      animation.opacity(1).step({duration: 300, transformOrigin: "50%,50%",timingFunction: 'linear'})
      that.setData({
        animationData: animation.export()
      })
    }.bind(this), 300)
  },
})
