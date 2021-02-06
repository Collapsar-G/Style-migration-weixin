const app = getApp();
Page({

  data: {
    cardCur: 0,
    swiperList: [{
      id: 0,
      type: 'image',
      url: '../../icon/qlssh.jpg'
    }, {
      id: 1,
        type: 'image',
        url: '../../icon/qjssh.jpg',
    }],
    src:'',
    btnheight:0,
    ljheight:0,
    bkheight:0,
    alpha:0,
    SPicWidth:0,
    SPicHeight:0,
    PicWidth:0,
    PicHeight:0,
    topMargin:0,
    leftMargin:0
  },
  onLoad() {
    let that = this
    wx.getSystemInfo({
      success: e => {
        let total = (e.windowHeight-app.globalData.CustomBar)*750/e.windowWidth
        console.log(total)
        that.setData({
          btnheight: total*0.29605263157894736842105263157895,
          ljheight: total*0.26315789473684210526315789473684,
          bkheight:total*0.61677631578947368421052631578947
        })
      }
    })
  },
  getLocalImage:function(){
    var that=this;
    wx.chooseImage({
        count:1,
        success:function(res){
            var filePath=res.tempFilePaths[0];
            wx.getImageInfo({
              src: filePath,
              success (res) {
                let twidth = res.width;
                let theight = res.height;
                let temp = 670/twidth*theight;
                if(temp>that.data.bkheight - 40){
                  let twid =(that.data.bkheight - 40)/theight*twidth
                  that.setData({
                    SPicWidth:twid,
                    SPicHeight:that.data.bkheight - 40,
                    PicHeight:theight,
                    PicWidth:twidth,
                    topMargin:40,
                    leftMargin:(750-twid)/2
                  })
                }
                else{
                  that.setData({
                    SPicWidth:670,
                    SPicHeight:temp,
                    PicHeight:theight,
                    PicWidth:twidth,
                    topMargin:20+(that.data.bkheight-temp)/2,
                    leftMargin:40
                  })
                }
              }
            })
            that.setData({
              src:filePath
            })
        },
        fail:function(error){
            console.error("调用本地相册文件时出错")
            console.warn(error)
        },
        complete:function(){

        }
    })
  },
  getChangeImage:function(){
    let that = this;
    let test =wx.getFileSystemManager().readFileSync(this.data.src, "base64")

    wx.request({
      url: 'http://xcx.collapsar.online/style_qlssh_no/',
      data: {
        comment_img:test,
        alpha:that.data.alpha
      },
      method: 'POST',
      success: (result)=>{
        console.log(result)
      },
      fail: ()=>{},
      complete: ()=>{}
    });
  },
  cardSwiper(e) {
    this.setData({
      cardCur: e.detail.current
    })
  },
})