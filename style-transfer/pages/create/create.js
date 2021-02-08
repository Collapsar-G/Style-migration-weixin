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
    alpha:0.5,
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
    keepColor:0
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
      loadModal: true
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
            that.setData({
              progessLoding: temp
            })
            if(that.data.progessLoding == 100){
              that.setData({
                lock : 0,
                tips:'生成成功',
              })
              clearInterval(that.data.setInter);
            }
        }
    , 200)
    wx.request({
      url: that.data.classList[that.data.keepColor][that.data.cardCur],
      data: {
        id:"111111",
        image:test,
        alpha:that.data.alpha
      },
      header: {
        'content-type': 'application/json' // 默认值
      },
      method: 'POST',
      success: (result)=>{
        that.setData({
          speed:3
        }),
        that.data.setInter2 = setInterval(
          function () {
              if(that.data.lock == 0){
                that.setData({
                  tips:'正在生成中...',
                  lock:1,
                  ShowProgress:0,
                  progessLoding:0,
                  speed:1,
                })
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
})