// pages/exhibition/exhibition.js
Page({

	/**
	 * 页面的初始数据
	 */
	data: {
		images:null,
		changes:[]
	},

	preview: function (event) {
		console.log(event.currentTarget.dataset.url)
		let currentUrl = event.currentTarget.dataset.url
		wx.previewImage({
			current: currentUrl, // 当前显示图片的http链接
			urls: [currentUrl] // 需要预览的图片http链接列表
		})
	},

	change:function(e){
		console.log(e)
		var index = e.currentTarget.dataset.index
		var value = e.detail.value
		this.setData({
			['changes['+index+']']:value
		})
	},

	getExhibition:function(e){
		const thiz = this

		wx.request({
			url: 'https://collapsar.cn.utools.club/show/show_all/',
			method:'GET',
			header:{
				'content-type':'application/json'
			},
			success: function (res){
				console.log(res)
				if(res.data.code==200){
					var changes = new Array(res.data.data.num)
					console.log(res.data.data.images)
					for (var i = 0; i < res.data.data.num; i++) {
						changes[i] = true
					}
					thiz.setData({
						images: res.data.data.images,
						changes: changes
					})

				}else{
					wx.showToast({
						title: '连接服务器失败',
						icon: 'error'
					})
				}

			},
			fail:function(res){
				wx.showToast({
					title: '连接服务器失败',
					icon:'error'
				})
			}
		})

	},

	/**
	 * 生命周期函数--监听页面加载
	 */
	onLoad: function (options) {
		this.getExhibition()
	},

	/**
	 * 生命周期函数--监听页面初次渲染完成
	 */
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