const express = require('express');
const http = require('http');
const app = express();
const server = http.createServer(app).listen(80);

// mid1
app.get('/mid1', function(req , res){
  res.sendfile("mid1.html");
})

// mid2
app.get('/mid2', function(req , res){
  res.sendfile("mid2.html");
})

// mid3
app.get('/mid3', function(req , res){
  res.sendfile("mid3.html");
})

// mid3 에서 서버로 데이터 전송시 받는 부분
app.get('/BMI', function(req , res){
  // 체중 cm → m로 변환
  let inputText1 = (Number(req.query.inputText1))/100;
  // 키
  let inputText2 = Number(req.query.inputText2);
  // BMI 계산
  let BMI = inputText2 / (inputText1*inputText1)
  // 초기 판정 결과
  let result = "오류";
  // 판정 결과 변경
  if (BMI < 20){
    result = "저체중"
  }else if(BMI < 25){
    result = "정상"
  }else if(BMI < 30){
    result = "과체중"
  }else if(BMI >= 30){
    result = "비만"
  }else{
    result = "숫자가 아닙니다"
  }
  // 보내기 전에 String로 변환
  BMI = String((parseInt(BMI*10))/10)
  // json 형식으로 BMI 랑 판정결과 보냄
  res.json({resultBMI1 : BMI , resultBMI2 : result});
})

// mid4
app.get('/mid4', function(req , res){
  res.sendfile("mid4.html");
})

// 서버에서 받을때 초기화 안되도록 밖에다 선언
// 학생 리스트
let studentList = [];
// 학생 수
let studentCount = 1;

// mid4 에서 서버로 데이터 전송시 받는 부분
app.get('/studentScore', function(req , res){
  // 각 점수 받기 
  let ko = Number(req.query.ko)*1;
  let eng = Number(req.query.eng)*2;
  let math = Number(req.query.math)*3;
  // 총점 계산
  let sumScore = ko + eng + math
  // 학생 한명 만들기
  let student = [studentCount ,sumScore];
  // 만든 학생 한명을 리스트에 넣기
  studentList.push(student);
  // 학생수 ++
  studentCount++;

  // 학생 점수기준 내림차순 정렬
  for (let i = 0; i < studentList.length; i++){
    for(let j = 0; j < studentList.length - i -1 ; j++){
      if(studentList[j][1] < studentList[j+1][1] ){
        let temp =  studentList[j+1];
        studentList[j+1] = studentList[j];
        studentList[j] = temp;
      }
    }
  }
  // 리스트 전송
  res.send(studentList);
})