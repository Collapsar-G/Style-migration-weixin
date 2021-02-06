const app = getApp();
Page({

  data: {
    cardCur: 0,
    swiperList: [{
      id: 0,
      type: 'image',
      url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big84000.jpg'
    }, {
      id: 1,
        type: 'image',
        url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big84001.jpg',
    }, {
      id: 2,
      type: 'image',
      url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big39000.jpg'
    }, {
      id: 3,
      type: 'image',
      url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big10001.jpg'
    }, {
      id: 4,
      type: 'image',
      url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big25011.jpg'
    }, {
      id: 5,
      type: 'image',
      url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big21016.jpg'
    }, {
      id: 6,
      type: 'image',
      url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big99008.jpg'
    }],
    src:'',
    btnheight:0,
    ljheight:0,
    bkheight:0,
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
            // 这里无论用户是从相册选择还是直接用相机拍摄，拍摄完成后的图片临时路径都会传递进来
            // app.startOperating("保存中")
            var filePath=res.tempFilePaths[0];
            that.setData({
              src:filePath
            })
            // var session_key=wx.getStorageSync('session_key');
            // // 这里顺道展示一下如何将上传上来的文件返回给后端，就是调用wx.uploadFile函数
            // wx.uploadFile({
            //     url: app.globalData.url+'/home/upload/uploadFile/session_key/'+session_key,
            //     filePath: filePath,
            //     name: 'file',
            //     success:function(res){
            //         app.stopOperating();
            //         // 下面的处理其实是跟我自己的业务逻辑有关
            //         var data=JSON.parse(res.data);
            //         if(parseInt(data.status)===1){
            //             app.showSuccess('文件保存成功');
            //         }else{
            //             app.showError("文件保存失败");
            //         }
            //     }
            // })
        },
        fail:function(error){
            console.error("调用本地相册文件时出错")
            console.warn(error)
        },
        complete:function(){

        }
    })
  }
})