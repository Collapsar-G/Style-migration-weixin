// pages/history/history.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    images:[],

  },

  preview: function(event) {
    console.log(event.currentTarget.dataset.url)
    let currentUrl = event.currentTarget.dataset.url
    wx.previewImage({
      current: currentUrl, // 当前显示图片的http链接
      urls: [currentUrl] // 需要预览的图片http链接列表
    })
  },

  formatTime: function(ts) {
    let tomorrow = new Date(parseInt(ts)*1000);
    let year = tomorrow.getFullYear(); //获取年
    let month = tomorrow.getMonth() + 1; //获取月
    let date = tomorrow.getDate(); //获取日
    let tomorrowSS = year + '-' + month + "-" + date
    return tomorrowSS
  },

  getHourAndMinute: function(ts) {
    let date = new Date(parseInt(ts)*1000)
    let hour = date.getHours()
    let minute = date.getMinutes()
    return hour + ":" + minute
  },

	saveImg: function (e) {
		if (this.data.HaveSave) {
			wx.showToast({
				title: '您已保存图片',
				icon: 'none',
				duration: 1500
			})
			return;
		}
		let that = this;

		//获取相册授权
		wx.getSetting({
			success(res) {
				if (!res.authSetting['scope.writePhotosAlbum']) {
					wx.authorize({
						scope: 'scope.writePhotosAlbum',
						success() {
							//这里是用户同意授权后的回调
							that.saveImgToLocal();
						},
						fail() {//这里是用户拒绝授权后的回调
							that.setData({
								openSettingBtnHidden: false
							})
						}
					})
				} else {//用户已经授权过了
					that.saveImgToLocal();
				}
			}
		})

	},
	saveImgToLocal: function (e) {
		let that = this;
		let imgSrc = that.data.src;
		wx.showLoading({
			title: '保存图片中',
		})
		console.log(imgSrc);
		wx.downloadFile({
			url: imgSrc,
			success: function (res) {
				//图片保存到本地
				wx.saveImageToPhotosAlbum({
					filePath: res.tempFilePath,
					success: function (data) {
						wx.hideLoading()
						wx.showToast({
							title: '保存成功',
							icon: 'success',
							duration: 2000
						})
						that.setData({
							HaveSave: 1
						})
					},
					fail: function (data) {
						wx.hideLoading()
						wx.showToast({
							title: '保存失败',
							icon: 'error',
							duration: 2000
						})
					}
				})
			}
		})

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

		wx.request({
			url: 'https://xcx.collapsar.online/user/history',
			method: 'GET',
			header: {
				'Cookie': app.globalData.cookie[0]
			},
			success: function (res) {
				console.log(res) //获取openid


				var json = res.data
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
					data.forEach(function (item) {
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

					thiz.setData({
						images: local_images
					})
				} else {
					//提示与服务器连接失败
				}


			},
			complete:function(res){

			}
		})

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