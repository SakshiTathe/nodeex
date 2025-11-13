const http=require('http');
const fs=require('fs');
const path=require('path');
const os=require('os');


function wfile(){
    fs.writeFileSync("mytxt.txt","Hello world",'utf-8')
    fs.readFileSync('mytxt.txt','utf-8',(err,data)=>{
        if(err){
            console.log("file not found");
            return ;
        }
    })
    fs.appendFileSync("mytxt.txt","\n hello world2");
    fs.open("input.txt", "r+", function (err, fd) {
	if (err) {
		return console.error(err);
	}
	console.log("File open successfully");
});
}

function allpaths(){
    console.log(__dirname);
    console.log(__filename);
    const filepa=path.join('folder','accor','to','os','slash','data.json');
    const parsedata=path.parse(filepa);
    const resolvee=path.resolve(filepa);
    const extnamee=path.extname(filepa);
    const basenamee=path.basename(filepa);
    const dirnamee=path.dirname(filepa);
    const reluse=path.join(__dirname,filepa);
    console.log({filepa,parsedata,resolvee,extnamee,basenamee,dirnamee});
    //we can use this for join for providing path while creating file
}
function osmod(){
    const hostname=os.hostname();
    const plat=os.platform();
    const arch=os.arch();
    const useinf=os.userInfo();
    const freemem=os.freemem();
    const ips=os.networkInterfaces;
    const cpus=os.cpus();
    console.log({hostname,plat,arch,useinf,freemem,ips,cpus});
}
function urlwork(){
    let adr = 'http://localhost:8080/default.htm?year=2017&month=february';
    let parsed=url.parse(adr,true);
    let dirurl=new url('http://localhost:8080/default.htm?year=2017&month=february');
    let hostn=parsed.hostname();
    let path=parsed.pathname();
}
//wfile();
//allpaths();
osmod();
const server=http.createServer((req,res)=>{
   res.end('Hello, World from Node.js Server!');
})
server.listen(3000,"localhost",()=>{
    console.log("server is started")
})