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
    TheOpacity: 1,
    canIUse:wx.canIUse('button.open-type.getUserInfo')
  },
  onLoad() {
    // 查看是否授权
    let that = this
    that.Login()
    // wx.getSetting({
    //   success (res){
    //     if (res.authSetting['scope.userInfo']) {
    //       // 已经授权，可以直接调用 getUserInfo 获取头像昵称
    //       that.Login()
    //       wx.getUserInfo({
    //         success: function(res) {
    //           console.log(res.userInfo)
    //         }
    //       })
    //       that.setData({
    //         canIUse:false
    //       })
    //     }
    //   }
    // })
  },
  onShow: function () {
    app.globalData.hasBackIndex = false
  },
  Login:function(){
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        var appid = 'wx7330267cab93fa97'; //填写微信小程序appid
        var secret = 'd2d27f80db202377fbb8ca9d49eab458'; //填写微信小程序secret
        //调用request请求api转换登录凭证
        wx.request({
          url: 'https://xcx.collapsar.online/user/login',
          data:{
            'code':res.code
          },
          method:'POST',
          header: {
            'content-type': 'application/json'
          },
          success: function (res) {
            console.log(res) //获取openid
            app.globalData.openid = res.data.id;
            app.globalData.hasLogin = true;
						app.globalData.cookie = res.cookies[0]
          }
        })
      }
    })
  },
  bindGetUserInfo (e) {
    if(e.detail.userInfo != null){
      this.Login();
      this.setData({
        canIUse:false
      })
    }
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
