// pages/history/history.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    images: [{
        "date": "",
        "array": [{
          'time': 11,
          "url": "rr"
        }]
      },
      {}
    ],
    test: {
      "code": 200,
      "data": [{
          "timestamp": "1612779210",
          "url": "http://127.0.0.1:3268/static/image/output/1612801118_stylized_qlssh_alpha_0.4_preserve_color_False.jpg"
        },
        {
          "timestamp": "1612777913",
          "url": "http://127.0.0.1:3268/static/image/output/1612801118_stylized_qlssh_alpha_0.4_preserve_color_False.jpg"
        }, {
          "timestamp": "1612479210",
          "url": "http://127.0.0.1:3268/static/image/output/1612801118_stylized_qlssh_alpha_0.4_preserve_color_False.jpg"
        },
        {
          "timestamp": "1612477913",
          "url": "http://127.0.0.1:3268/static/image/output/1612801118_stylized_qlssh_alpha_0.4_preserve_color_False.jpg"
        }
      ],
      "msg": "success"
    }
  },

  formatTime: function(ts) {
    let tomorrow = new Date(parseInt(ts) * 1000);
    let year = tomorrow.getFullYear(); //获取年
    let month = tomorrow.getMonth() + 1; //获取月
    let date = tomorrow.getDate(); //获取日
    let tomorrowSS = year + '-' + month + "-" + date
    return tomorrowSS
  },

  getHourAndMinute: function(ts) {
    let date = new Date(parseInt(ts) * 1000)
    let hour = date.getHours()
    let minute = date.getMinutes()
    return hour + ":" + minute
  },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    // wx.request({
    //   url: 'https://xcx.collapsar.online/user/history',
    //   method: 'GET',
    //   success: function(res) {
    //     console.log(res) //获取history

    //   }
    // })
    var thiz = this
    var json = thiz.data.test
    var code = json.code
    var data = json.data
    console.log(data)
    if (code == 200) {
      //正常返回，处理时间戳变成时间
      let last_date = thiz.formatTime(data[0].timestamp)
      let itemJson = new Object()
      itemJson['date'] = ''
      itemJson['array'] = []
      let local_images = []
      data.forEach(function(item) {
        console.log(item)
        var timestamp = item.timestamp
        var url = item.url
        var date = thiz.formatTime(timestamp)
        console.log(last_date)
        console.log(date)
        if (!(date === last_date)) {
          local_images.push(itemJson)
          itemJson = new Object()
          itemJson['date'] = ''
          itemJson['array'] = []
        }
        itemJson["date"] = date
				let image_json = new Object()
				image_json["time"] = thiz.getHourAndMinute(timestamp)
				image_json["url"] = url
        itemJson["array"].push(image_json)

        last_date = date
      })

      local_images.push(itemJson)
      console.log('loc', local_images)

      thiz.setData({
        images: local_images
      })
    } else {
      //提示与服务器连接失败
    }
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