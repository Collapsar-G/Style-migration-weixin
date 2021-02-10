// pages/feedback/feedback.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },
  /**
   * 点击发送反馈
   */
  sendFeedback() {
    const thiz = this
    let inputValue = thiz.data.inputValue
    console.log("inputvalue", inputValue)
    if (inputValue) {
      wx.showModal({
        title: '确认',
        content: '是否确认发送信息',
        showCancel: true,
        success: function(res) {
          console.log("res", res)
          if (res.confirm) {
            wx.showLoading({
              title: '发送中',
            })

            wx.request({
              url: 'https://xcx.collapsar.online/feedback/feedback_content',
              data: {
                'content': inputValue
              },
              method: 'POST',
              header: {
                'content-type': 'application/json'
              },
              success: function(res) {
                console.log(res) //获取openid
                if (res.data.code == 200) {
                  wx.showModal({
                    title: '回应',
                    content: '感觉您的反馈，我们会尽快处理',
                  })
                  thiz.setData({
                    inputValue: null
                  })
                } else {
                  wx.showModal({
                    title: '回应',
                    content: '服务器异常，发送失败',
                  })
                }
              },
              fail: function(res) {
                wx.showModal({
                  title: '回应',
                  content: '服务器异常，发送失败',
                })
              },
              complete: function(res) {
                wx.hideLoading()
              }
            })

          }

        },
      })
    } else {
      wx.showModal({
        title: '警告',
        content: '所发信息内容不能为空'
      })
    }


  },

  textareaInputListener(e) {
    let inputValue = e.detail.value
    this.setData({
      inputValue: inputValue
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  }
})