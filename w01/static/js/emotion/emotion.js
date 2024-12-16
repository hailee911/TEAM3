window.onload = function () {
   const graphs = [
       {
           selector: ".emotion_graph_mm",
           url: '/emotion/main_data1/',
           barColor: "#7D7D7D",
           lineColor: "#001DFF",
       },
       {
           selector: ".emotion_graph_ww",
           url: "/emotion/main_data2/",
           barColor: "#7D7D7D",
           lineColor: "#001DFF",
           useLabels: true,
       },
       {
           selector: ".family_graph_ll",
           url: '/emotion/main_data1/',
           barColor: "#F4A79D",
           lineColor: null,
       },
       {
           selector: ".personal_graphh",
           url: '/emotion/main_data5/',
           barColor: "#344BFD",
           lineColor: null,
       },
       
   ];

   const commonHeight = 280;
   const padding = 30;

   // 데이터 가져오기
   function fetchData(url) {
      return fetch(url)
         .then(response => response.json())
         .catch(error => {
            console.error("Error fetching data:", error);
            return []; // 오류 발생 시 빈 배열 반환
         });
   }

   function drawBarChart({ selector, data, barColor, lineColor, useLabels = false }) {
       const container = document.querySelector(selector);
       const svg = d3.select(container).append("svg");

       function updateSize() {
           const width = container.offsetWidth;
           svg.attr("width", width).attr("height", commonHeight);

           const xScale = d3.scaleBand()
               .rangeRound([padding, width - padding])
               .padding(0.5)
               .domain(data.map(d => d.name));

           const yScale = d3.scaleLinear()
               .domain([0, 100])
               .range([commonHeight - padding, padding]);

           svg.selectAll("*").remove();

           // Draw axis
           const xAxis = d3.axisBottom(xScale).tickSize(0);
           svg.append("g")
               .attr("transform", `translate(0,${commonHeight - padding + 5})`)
               .call(xAxis);

           svg.selectAll(".tick text")
               .each(function (d) {
                   if (useLabels) {
                       const datum = data.find(item => item.name === d);
                       const text = d3.select(this);
                       text.text("");
                       text.append("tspan")
                       .text(datum.name)
                       .attr("x", 0)
                       .attr("dy", "0em")
                       .attr("class", "value-text");
                       text.append("tspan")
                       .text(datum.label)
                       .attr("x", 0)
                       .attr("dy", "1.2em")
                   }
               })
               .attr("transform", "translate(0, 5)"); 

           svg.selectAll("path.domain").remove();

           // Draw vertical lines
           svg.selectAll(".vertical-line")
               .data(data)
               .enter()
               .append("line")
               .attr("class", "vertical-line")
               .attr("x1", d => xScale(d.name) + xScale.bandwidth() / 2)
               .attr("x2", d => xScale(d.name) + xScale.bandwidth() / 2)
               .attr("y1", commonHeight - padding)
               .attr("y2", padding);

           // Draw bars
           svg.selectAll(".bar")
               .data(data)
               .enter()
               .append("rect")
               .attr("class", "bar")
               .attr("x", d => xScale(d.name))
               .attr("y", d => yScale(d.value))
               .attr("width", xScale.bandwidth())
               .attr("height", d => commonHeight - padding - yScale(d.value))
               .attr("fill", barColor)
               .attr("rx", 15)
               .attr("ry", 15); 

           // Draw values
           svg.selectAll(".value_text")
               .data(data)
               .enter()
               .append("text")
               .attr("class", "value-text")
               .attr("x", d => xScale(d.name) + xScale.bandwidth() / 2)
               .attr("y", padding / 2 )
               .attr("text-anchor", "middle")
               .text(d => d.value);

           // Draw line
           if (lineColor) {
               const line = d3.line()
                   .x(d => xScale(d.name) + xScale.bandwidth() / 2)
                   .y(d => yScale(d.value));

               svg.append("path")
                   .datum(data)
                   .attr("fill", "none")
                   .attr("stroke", lineColor)
                   .attr("stroke-width", 1)
                   .attr("d", line);
           }
       }

       updateSize();
       window.addEventListener("resize", updateSize);
   }


  // 파이차트 좋아요 
  function drawPieChart({ selector, data }) {
      const container = document.querySelector(selector);
      const width = container.offsetWidth;
      const height = 280;
      const radius = Math.min(width, height) / 3;

      const svg = d3.select(container)
         .append("svg")
         .attr("width", width)
         .attr("height", height + 50)
         .append("g")
         .attr("transform", `translate(${width / 2}, 90)`);

      const color = d3.scaleOrdinal(d3.schemeSet2);
      const pie = d3.pie().value(d => d.value);
      const arc = d3.arc().outerRadius(radius - 10).innerRadius(0);

      const pieData = pie(data);

      svg.selectAll(".arc")
         .data(pieData)
         .enter()
         .append("g")
         .attr("class", "arc")
         .append("path")
         .attr("d", arc)
         .attr("fill", (d, i) => color(i));

      // Add Legend
      const legend = svg.append("g")
         .attr("transform", `translate(-${radius - 15}, ${height / 3 + 10})`);

      const totalValue = d3.sum(data, d => d.value);

      legend.selectAll(".legend-item")
         .data(data)
         .enter()
         .append("g")
         .attr("class", "legend-item")
         .attr("transform", (d, i) => `translate(20, ${i * 25})`)
         .each(function(d, i) {
            const group = d3.select(this);
            group.append("rect")
               .attr("x", 0)
               .attr("width", 15)
               .attr("height", 15)
               .attr("fill", color(i));
               
            const percentage = ((d.value / totalValue) * 100).toFixed(1);
            group.append("text")
               .attr("x", 20)
               .attr("y", 12)
               .text(`${d.name} (${percentage}%)`);
         });

      // Resize functionality for Pie chart
      function updateSize() {
         const width = container.offsetWidth;
         const height = 280;
         const radius = Math.min(width, height) / 3;

         svg.attr("width", width).attr("height", height + 80);

         svg.selectAll("path")
            .attr("d", arc.outerRadius(radius - 10).innerRadius(0));
      }

      window.addEventListener("resize", updateSize);
      updateSize(); // Initial size adjustment
   }


   // 데이터 가져와서 그래프 그리기
   function loadGraphsData() {
      const pieDataUrl = "/emotion/main_data4/"; // 예시 데이터 URL
      const pieData = fetchData(pieDataUrl);

      pieData.then(data => {
            drawPieChart({ selector: ".family_graph_rr", data: data });
      });

      graphs.forEach(graph => {
            fetchData(graph.url).then(data => {
               drawBarChart({
                  selector: graph.selector,
                  data: data,
                  barColor: graph.barColor,
                  lineColor: graph.lineColor,
                  useLabels: graph.useLabels
               });
            });
      });
   }

  loadGraphsData();
};

