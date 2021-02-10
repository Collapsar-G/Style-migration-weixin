const app = getApp();
Page({

  data: {
    cardCur: 0,
    swiperList: [{
      id: 0,
      type: 'image',
      url: '../../icon/qlssh.jpg',
      name: '《青绿山水图》'
    }, {
      id: 1,
        type: 'image',
        url: '../../icon/qjssh.jpg',
        name: '《浮玉山居图》'
    }],
    classList:[["https://xcx.collapsar.online/transfer/style_qlssh_no",
    "https://xcx.collapsar.online/transfer/style_qjssh_no"
    ],
    [
      "https://xcx.collapsar.online/transfer/style_qlssh_is",
      "https://xcx.collapsar.online/transfer/style_qjssh_is"
    ]],
    IsExist:0,
    src:'',
    PicType:'',
    btnheight:0,
    ljheight:0,
    bkheight:0,
    alpha:50,
    SPicWidth:0,
    SPicHeight:0,
    PicWidth:0,
    PicHeight:0,
    topMargin:0,
    leftMargin:0,
    InsertPicWidth:500,
    InsertPicHeight:0,
    InsertPicTopMargin:0,
    InsertPicLeftMargin:0,
    loadModal:false,
    animationData:{},
    progessLoding:0,
    speed:1,
    ShowProgress:0,
    tips:'正在生成中...',
    lock:1,
    keepColor:0,
    hideDisplay:'',
    success:0,
    getReply:0,
    showBtn:1,
    openSettingBtnHidden:true,
    HaveSave:0
  },
  onLoad() {
    let that = this
    let bkss = 0
    wx.getSystemInfo({
      success: e => {
        let total = (e.windowHeight-app.globalData.CustomBar)*750/e.windowWidth
        that.setData({
          btnheight: total*0.29605263157894736842105263157895,
          ljheight: total*0.26315789473684210526315789473684,
          bkheight:total*0.61677631578947368421052631578947
        })
        bkss = total*0.61677631578947368421052631578947
      }
    })

    wx.getImageInfo({
      src: "../../icon/picture2.png",
      success (res) {
        let twidth = 500;
        let theight = 500;
        let temp = 500/twidth*theight;
        if(temp>bkss - 40){
          let twid =(bkss - 40)/theight*twidth
          that.setData({
            InsertPicWidth:twid,
            InsertPicHeight:bkss - 40,
            InsertPicTopMargin:40,
            InsertPicLeftMargin:(750-twid)/2
          })
        }
        else{
          that.setData({
            InsertPicWidth:500,
            InsertPicHeight:temp,
            InsertPicTopMargin:20+(bkss-temp)/2,
            InsertPicLeftMargin:125
          })
        }
      }
    })
  },
  showModal(e) {
    this.setData({
      modalName: e.currentTarget.dataset.target
    })
  },
  hideModal() {
    this.setData({
      modalName: null
    })
  },
  showModal2(e) {
    this.setData({
      modalName2: e.currentTarget.dataset.target
    })
  },
  hideModal2() {
    this.setData({
      modalName2: null
    })
  },
  changeStatus:function(){
    let change = 1 - this.data.IsExist;
    this.setData({
      IsExist:change
    })
  },
  changeKeepColor(){
    let temp = 1-this.data.keepColor
    this.setData({
      keepColor:temp
    })
    if(temp){
      wx.showToast({
        title: '保留原图色彩',
        icon: 'success',
        duration: 1000
      })
    }
    else{
      wx.showToast({
        title: '不保留原图色彩',
        icon: 'error',
        duration: 1000
      })
    }
    setTimeout(()=> {
      wx.hideToast();
    },1000)

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
                    leftMargin:(750-twid)/2,
                    PicType:res.type
                  })
                }
                else{
                  that.setData({
                    SPicWidth:670,
                    SPicHeight:temp,
                    PicHeight:theight,
                    PicWidth:twidth,
                    topMargin:20+(that.data.bkheight-temp)/2,
                    leftMargin:40,
                    PicType:res.type
                  })
                }
              }
            })
            that.setData({
              src:filePath,
              IsExist: 1
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
    this.setData({
      loadModal: true,
      hideDisplay: "block"
    })
    let that = this;
    let test ="data:image/"+this.data.PicType+";base64,"+wx.getFileSystemManager().readFileSync(this.data.src, "base64")
    this.hideModal();
    setTimeout(()=> {
      this.setData({
        loadModal: false,
        ShowProgress: 1,
        lock : 1
      })
    }, 500)
     //将计时器赋值给setInter
    that.data.setInter = setInterval(
        function () {
            let temp = that.data.progessLoding + that.data.speed;
            temp = temp>100?100:temp
            if(that.data.progessLoding == 100){
                if(that.data.getReply){
                  if(that.data.success){
                    that.setData({
                      lock : 0,
                      tips:'生成成功',
                    })
                  }
                  else{
                    that.setData({
                      lock : 0,
                      tips:'生成失败',
                    })
                  }
                  clearInterval(that.data.setInter);
                }
            }
            else{
              that.setData({
                progessLoding: temp
              })
            }
        }
    , 200)
    wx.request({
      url: that.data.classList[that.data.keepColor][that.data.cardCur],
      data: {
        id:app.globalData.openid,
        image:test,
        alpha:that.data.alpha/100
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      method: 'POST',
      success: (result)=>{
        if(result.data.code !=200){
          that.setData({
            speed:3,
            success:0,
            getReply:1
          })
        }
        else{
          that.setData({
            speed:3,
            success:1,
            getReply:1
          })
        }
        that.data.setInter2 = setInterval(
          function () {
              if(that.data.lock == 0){
                if(that.data.success){
                  that.setData({
                    tips:'正在生成中...',
                    lock:1,
                    ShowProgress:0,
                    progessLoding:0,
                    hideDisplay:'',
                    speed:1,
                    src:result.data.url,
                    success:0,
                    getReply:0,
                    showBtn:0,
                    alpha:50
                  })
                }
                else{
                  that.setData({
                    tips:'正在生成中...',
                    lock:1,
                    ShowProgress:0,
                    progessLoding:0,
                    hideDisplay:'',
                    speed:1,
                    success:0,
                    getReply:0,
                    alpha:50
                  })
                }
                clearInterval(that.data.setInter2);
              }
          }
        , 200)
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
  catchtouchmove(){
  },
  slider(e){
    this.setData({
      alpha:e.detail.value
    })
  },
  closeCreate:function(){
    this.hideModal2()
    this.setData({
      IsExist:0,
      showBtn:1,
      src:'',
      HaveSave:0
    })
  },
  saveImg:function(e){
    if(this.data.HaveSave){
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
              HaveSave:1
            })
          },
          fail:function(data){
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

})