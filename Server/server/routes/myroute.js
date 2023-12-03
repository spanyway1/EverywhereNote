var express = require('express');
const { fstat } = require('fs');
var router = express.Router();
var fs = require('fs');

//파일을 읽고 클라이언트에 전달하는 GET 메서드
router.get('/getFile', function(req, res, next){
    console.log('getFile 호출 / data : \n');
    console.log(req.query);
    
    //소스폴더에 notes 폴더에 있는 내용을 읽습니다.
    // req.query에 중 id 중 fileName을 가져옵니다.
    fs.readFile('/home/server/notes/' + req.query.fileName, 'utf-8', function(err, readdata){
        if(err){
            res.send("ERR");
        }else{
            console.log('read end');
            console.log(readdata);
            //읽은 내용을 클라이언트에 전송합니다.
            res.send(readdata);
        }
    });
});

//파일 목록을 읽고 클라이언트에 전달하는 GET 메서드
router.get('/getFileList', function(req, res, next){
    console.log('getFileList 호출 : \n');
    getFiles(res)
});

//파일 목록들을 가져와서 반환하는 메서드
let getFiles = (res)=>{
    //소스폴더에 notes 폴더에 있는 파일들을 읽습니다.
    fs.readdir('/home/server/notes/', function(error, filelist){
        if(error){
            return "ERR";
        }
        console.log(filelist);
        //파일이 존재하면
        if(filelist !=undefined)
        {
            let data = "";
            //list로 전달되는 filelist를 for 문으로 처리합니다.
            for(let i = 0; i < filelist.length; i++){
                data = data + filelist[i]+ '\n';
            }
            res.send(data);
        }else
        {
            //파일이 없기 때문에 공백으로 전송합니다.
            res.send("");
        }
    });
};

//전달된 fileName과 text로 파일을 생성하는 POST 메서드
router.post('/saveFile', function(req, res, next){
    console.log('saveFile 호출 / data: \n');

    //전달된 json을 data 저장합니다.
    let data = req.body;
    let file_ = "/home/server/notes/"+data.fileName;
    //파일로 저장합니다.
    fs.writeFile(file_, data.text, 'utf-8', function(err){
        if(err){
            console.log(err);
            res.send("ERR");
        }else{
            console.log('write end');
            res.send("OK");
        }
    });
});

// 전달된 fileName에 해당하는 파일을 제거하는 메서드
router.get('/deleteFile', function(req, res, next){
    console.log('deleteFile 호출 / fileName: \n' + '/home/server/notes/' +  req.query.fileName);
    //동기식으로 파일을 제거합니다.
    fs.unlink('/home/server/notes/' +  req.query.fileName,(err)=>{
        if(err){
            console.log(err);
            res.send("ERR");
        }else{
            console.log("종료");
            res.send("OK");
        }
    });
});

module.exports = router;