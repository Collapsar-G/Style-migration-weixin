// pages/login/login.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    isHide: true
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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
            wx.switchTab({
              url: '../../pages/myhome/myhome'
            })
          }
        })
      }
    })
  },
  bindGetUserInfo (e) {
    if(e.detail.userInfo != null){
      this.Login();
    }
  },
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    if(app.globalData.hasLogin){
      wx.switchTab({
        url: '../../pages/myhome/myhome'
      })
    }
    else{
      app.globalData.hasBackIndex = true
      wx.switchTab({
        url: '../../pages/index/index'
      })
    }
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})