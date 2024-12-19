// 데이터 불러오기

// 상단 그래프 만들기
window.onload = function() {
  // 데이터와 그래프 설정
  var dataset = [
      { "name": "1주", "value": 5 },
      { "name": "2주", "value": 6 },
      { "name": "3주", "value": 8 },
      { "name": "4주", "value": 1 },
      { "name": "5주", "value": 2 },
  ];

  var height = 280; // 고정된 높이
  var padding = 30;

  // SVG 요소 생성 (초기 크기 설정)
  // 월 감정 그래프 
  var svg = d3.select(".emotion_graph_mm")
              .append("svg");

  // resize 이벤트 리스너 추가
  function updateGraphSize() {
      // div의 너비를 동적으로 가져오기
      var divWidth = document.querySelector(".emotion_graph_mm").offsetWidth;

      // SVG의 크기 업데이트
      svg.attr("width", divWidth)  // div의 크기 기반으로 width 설정
         .attr("height", height);  // 고정된 높이 사용

      // xScale과 yScale 다시 설정
      var xScale = d3.scaleBand()
                     .rangeRound([padding, divWidth - padding]) // div 너비에 맞춰 설정
                     .padding(0.5)
                     .domain(dataset.map(function(d) { return d.name; }));

      var yScale = d3.scaleLinear()
                     .domain([0, d3.max(dataset, function(d) { return d.value; })])
                     .range([height - padding, padding]);

      // 기존 그래프를 지우고 새로 그리기
      svg.selectAll("*").remove(); // 기존 그래프 요소를 모두 제거

      // 축 추가
      svg.append("g")
         .attr("transform", "translate(0," + (height - padding + 12) + ")")
         .call(d3.axisBottom(xScale).tickSize(0))
         .selectAll(".tick text")  // 각 레이블을 선택
         .attr("font-size", "14px")  // 글자 크기 설정
         .attr("font-weight", "bold")  // 글자 굵기 설정
         .attr("fill", "black");  // 글자 색상 설정;

      // domain 선 제거
      svg.selectAll("path.domain").remove(); 

      // 세로 줄 생성
      svg.selectAll(".vertical-line")
      .data(dataset)
      .enter()
      .append("line")
      .attr("class", "vertical-line")
      .attr("x1", d => xScale(d.name) + xScale.bandwidth() / 2)
      .attr("x2", d => xScale(d.name) + xScale.bandwidth() / 2)
      .attr("y1", height - padding  - 10)
      .attr("y2", padding)
      .attr("stroke", "#B1B1B1")
      .attr("stroke-width", 0.5)

      // 막대 그래프 추가
      svg.selectAll("rect")
         .data(dataset)
         .enter()
         .append("rect")
         .attr("x", function(d) { return xScale(d.name); })
         .attr("y", function(d) { return yScale(d.value)  - 10; })
         .attr("width", xScale.bandwidth())
         .attr("height", function(d) { return height - padding - yScale(d.value); })
         .attr("fill", "#7D7D7D")
         .attr("rx", 15)  // 좌우 모서리 둥글기
         .attr("ry", 15) // 상하 모서리 둥글기;
         ; 

      // 각 막대 위에 값 표시
      svg.selectAll("text11")
         .data(dataset)
         .enter()
         .append("text")
         .attr("x", d => xScale(d.name) + xScale.bandwidth() / 2)
         .attr("y", padding / 2 )
         .attr("text-anchor", "middle")
         .attr("fill", "#797979")
         .style("font-size", "12px") // 글자 크기
         .text(function(d) { return d.value; });

      var line = d3.line()
      .x(function(d) { return xScale(d.name) + xScale.bandwidth() / 2; }) // 막대의 중심 x 좌표
      .y(function(d) { return yScale(d.value); }); // 막대 꼭짓점 y 좌표
      
      // 선 추가
      svg.append("path")
         .datum(dataset) // 데이터를 path에 바인딩
         .attr("fill", "none") // 채우기 없음
         .attr("stroke", "#001DFF") // 선 색상
         .attr("stroke-width", 1) // 선 두께
         .attr("d", line); // 라인 제너레이터를 사용하여 선을 그림

  }


  // 데이터와 그래프 설정 - 2번째 그래프
  var dataset2 = [
   { "name1": "11", "name2": "월", "value": 40 },
   { "name1": "12", "name2": "화", "value": 60 },
   { "name1": "13", "name2": "수", "value": 99 },
   { "name1": "14", "name2": "목", "value": 54 },
   { "name1": "15", "name2": "금", "value": 78 },
   { "name1": "16", "name2": "토", "value": 40 },
   { "name1": "17", "name2": "일", "value": 30 },
  ];



  // SVG 요소 생성 (초기 크기 설정)
  // 월 감정 그래프 
  var svg2 = d3.select(".emotion_graph_ww")
              .append("svg");

  // resize 이벤트 리스너 추가
  function updateGraphSize2() {
      // div의 너비를 동적으로 가져오기
      var divWidth2 = document.querySelector(".emotion_graph_ww").offsetWidth;

      // SVG의 크기 업데이트
      svg2.attr("width", divWidth2)  // div의 크기 기반으로 width 설정
         .attr("height", height);  // 고정된 높이 사용

      // xScale과 yScale 다시 설정
      var xScale2 = d3.scaleBand()
                     .rangeRound([padding, divWidth2 - padding]) // div 너비에 맞춰 설정
                     .padding(0.5)
                     .domain(dataset2.map(function(d) { return d.name1; }));

      var yScale2 = d3.scaleLinear()
                     .domain([0, d3.max(dataset2, function(d) { return d.value ; })])
                     .range([height - padding, padding]);

      // 기존 그래프를 지우고 새로 그리기
      svg2.selectAll("*").remove(); // 기존 그래프 요소를 모두 제거

      // 축 추가
      svg2.append("g")
         .attr("transform", "translate(0," + (height - padding + 9) + ")")
         .call(d3.axisBottom(xScale2).tickSize(0));

      svg2.selectAll(".tick text")
      .attr("font-size", "14px")
      .attr("font-weight", "bold")
      .attr("fill", "black")
      .each(function(d) {
            // d는 "name1"이므로, d에 "name2"를 붙여서 두 줄로 나누어 표시
            var data = dataset2.find(item => item.name1 === d); // d와 일치하는 데이터를 찾음
            var name1 = data.name1;
            var name2 = data.name2;
            
            // tspan을 추가하기 전에 기존 text를 먼저 다루고 텍스트에 대한 설정을 수정합니다.
            var text = d3.select(this); // text 요소를 선택

            // 첫 번째 줄 (name1)
            text.text(""); // 기존 텍스트 제거 (여기서 첫 번째 줄을 설정)
            text.append("tspan")
               .attr("x", 0)
               .attr("dy", "0em") // 첫 번째 줄 위치
               .text(name1)
               .attr("font-size", "12px")
               .attr("font-weight", "normal")
               .attr("fill", "#797979");
               
               // 두 번째 줄 (name2)
               text.append("tspan")
               .attr("x", 0)
               .attr("dy", "1.2em") // 두 번째 줄 위치
               .text(name2)
               .attr("font-size", "14px")  // 다른 스타일 적용
               .attr("font-weight", "bold")
               .attr("fill", "black");  // 다른 색상 설정
         });

      // domain 선 제거
      svg2.selectAll("path.domain").remove(); 

      // 세로 줄 생성
      svg2.selectAll(".vertical-line")
      .data(dataset2)
      .enter()
      .append("line")
      .attr("class", "vertical-line")
      .attr("x1", d => xScale2(d.name1) + xScale2.bandwidth() / 2)
      .attr("x2", d => xScale2(d.name1) + xScale2.bandwidth() / 2)
      .attr("y1", height - padding - 10)
      .attr("y2", padding)
      .attr("stroke", "#B1B1B1")
      .attr("stroke-width", 0.5)

      // 막대 그래프 추가
      svg2.selectAll("rect")
         .data(dataset2)
         .enter()
         .append("rect")
         .attr("x", function(d) { return xScale2(d.name1); })
         .attr("y", function(d) { return yScale2(d.value) - 10; })
         .attr("width", xScale2.bandwidth())
         .attr("height", function(d) { return height - padding - yScale2(d.value); })
         .attr("fill", "#7D7D7D")
         .attr("rx", 15)  // 좌우 모서리 둥글기
         .attr("ry", 15) // 상하 모서리 둥글기;
         ;

      // 각 막대 위에 값 표시
      svg2.selectAll("text22")
         .data(dataset2)
         .enter()
         .append("text")
         .attr("x", d => xScale2(d.name1) + xScale2.bandwidth() / 2)
         .attr("y", padding / 2 )
         .attr("text-anchor", "middle")
         .attr("fill", "#797979")
         .style("font-size", "12px") // 글자 크기
         .text(function(d) { return d.value; });

      var line2 = d3.line()
      .x(function(d) { return xScale2(d.name1) + xScale2.bandwidth() / 2; }) // 막대의 중심 x 좌표
      .y(function(d) { return yScale2(d.value); }); // 막대 꼭짓점 y 좌표
      
      // 선 추가
      svg2.append("path")
         .datum(dataset2) // 데이터를 path에 바인딩
         .attr("fill", "none") // 채우기 없음
         .attr("stroke", "#001DFF") // 선 색상
         .attr("stroke-width", 1) // 선 두께
         .attr("d", line2); // 라인 제너레이터를 사용하여 선을 그림
  }

  /////// 하단 그래프
  // 하단 댓글 수 그래프 (도넛)
  var dataset3 = [
   { "name": "배현지", "value": 7 },
   { "name": "이다영", "value": 11 },
   { "name": "장서윤", "value": 88 },
   { "name": "정종원", "value": 16 },
  ]

  var height = 280; // 고정된 높이
  var margin = 40;  // 여백
  var width = 250;
   // 반지름 계산
  var radius = Math.min(width, height) / 2 - margin;

   // 전체 합계 계산
   var totalValue = d3.sum(dataset3, function(d) { return d.value; });

   // SVG 요소 추가
   var svg3 = d3.select(".family_graph_rr")
               .append("svg")
               .attr("width", width)
               .attr("height", height)
               .append("g")
               .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");  // 중앙 배치

   // pie 차트 레이아웃 생성
   var pie = d3.pie()
               .value(function(d) { return d.value; })
               .sort(null);

   // arc 설정 (도넛 그래프)
   var arc = d3.arc()
               .innerRadius(radius - 50) // 내부 반지름
               .outerRadius(radius);  // 외부 반지름

   // 색상 스케일
   var color = d3.scaleOrdinal(d3.schemeCategory10);

   // arc 요소 추가하여 파이 조각 생성
   var arcs = svg3.selectAll(".arc")
                 .data(pie(dataset3))
                 .enter()
                 .append("path")
                 .attr("class", "arc")
                 .attr("d", arc)
                 .attr("fill", function(d, i) { return color(i); }); // 색상 지정


   // 크기 업데이트 함수
   function updateGraphSize3() {
      // div의 새로운 크기 가져오기
      var divWidth3 = document.querySelector(".family_graph_rr").offsetWidth;
      var divHeight3 = divWidth3;  // 정사각형 차트로 설정
      }
    

  // 하단 좋아요 수 그래프
  // 데이터와 그래프 설정
  var dataset4 = [
   { "name": "배현지", "value": 77 },
   { "name": "이다영", "value": 11 },
   { "name": "장서윤", "value": 88 },
   { "name": "정종원", "value": 16 },
   ];

   var height = 280; // 고정된 높이
   var padding = 30;

   // SVG 요소 생성 (초기 크기 설정)
   // 월 감정 그래프 
   var svg4 = d3.select(".family_graph_ll")
            .append("svg");

   // resize 이벤트 리스너 추가
   function updateGraphSize4() {
      // div의 너비를 동적으로 가져오기
      var divWidth4 = document.querySelector(".family_graph_ll").offsetWidth;

      // SVG의 크기 업데이트
      svg4.attr("width", divWidth4)  // div의 크기 기반으로 width 설정
         .attr("height", height);  // 고정된 높이 사용

      // xScale과 yScale 다시 설정
      var xScale4 = d3.scaleBand()
                     .rangeRound([padding, divWidth4 - padding]) // div 너비에 맞춰 설정
                     .padding(0.6)
                     .domain(dataset4.map(function(d) { return d.name; }));

      var yScale4 = d3.scaleLinear()
                     .domain([0, d3.max(dataset4, function(d) { return d.value; })])
                     .range([height - padding, padding]);

      // 기존 그래프를 지우고 새로 그리기
      svg4.selectAll("*").remove(); // 기존 그래프 요소를 모두 제거

      // 축 추가
      svg4.append("g")
         .attr("transform", "translate(0," + (height - padding + 12) + ")")
         .call(d3.axisBottom(xScale4).tickSize(0))
         .selectAll(".tick text")  // 각 레이블을 선택
         .attr("font-size", "14px")  // 글자 크기 설정
         .attr("font-weight", "bold")  // 글자 굵기 설정
         .attr("fill", "black");  // 글자 색상 설정;

      // domain 선 제거
      svg4.selectAll("path.domain").remove(); 

      // 세로 줄 생성
      svg4.selectAll(".vertical-line")
      .data(dataset4)
      .enter()
      .append("line")
      .attr("class", "vertical-line")
      .attr("x1", d => xScale4(d.name) + xScale4.bandwidth() / 2)
      .attr("x2", d => xScale4(d.name) + xScale4.bandwidth() / 2)
      .attr("y1", height - padding  - 10)
      .attr("y2", padding)
      .attr("stroke", "#B1B1B1")
      .attr("stroke-width", 0.5)

      // 막대 그래프 추가
      svg4.selectAll("rect")
         .data(dataset4)
         .enter()
         .append("rect")
         .attr("x", function(d) { return xScale4(d.name); })
         .attr("y", function(d) { return yScale4(d.value)  - 10; })
         .attr("width", xScale4.bandwidth())
         .attr("height", function(d) { return height - padding - yScale4(d.value); })
         .attr("fill", "#F4A79D")
         .attr("rx", 15)  // 좌우 모서리 둥글기
         .attr("ry", 15); // 상하 모서리 둥글기;

      // 각 막대 위에 값 표시
      svg4.selectAll("text44")
         .data(dataset4)
         .enter()
         .append("text")
         .attr("x", d => xScale4(d.name) + xScale4.bandwidth() / 2)
         .attr("y", padding / 2 )
         .attr("text-anchor", "middle")
         .attr("fill", "#797979")
         .style("font-size", "12px") // 글자 크기
         .text(function(d) { return d.value; });

      
   }

  // 페이지 로드 시 초기 크기 설정
  updateGraphSize();
  updateGraphSize2();
  updateGraphSize3();
  updateGraphSize4();

  // resize 이벤트가 발생할 때마다 그래프 크기 갱신
  window.onresize = function() {
      updateGraphSize();
      updateGraphSize2();
      updateGraphSize3();
      updateGraphSize4();
   };

};
