document.addEventListener('DOMContentLoaded', function() {
    // Navigation scroll behavior
    const navLinks = document.querySelectorAll('nav a, .footer-links a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.getAttribute('href').startsWith('#')) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // Set active menu item based on URL
    const currentUrl = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-links a');
    
    navItems.forEach(item => {
        const href = item.getAttribute('href');
        // If it's an exact match or if it's a section of the current page
        if (href === currentUrl || (currentUrl === '/' && href.startsWith('#'))) {
            item.classList.add('active');
        }
    });
    
    // Navigation background change on scroll
    const nav = document.querySelector('nav');
    
    function updateNavBackground() {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    }
    
    window.addEventListener('scroll', updateNavBackground);
    updateNavBackground();
    
    // Mobile menu toggle
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const navLinksContainer = document.querySelector('.nav-links');
    
    if (hamburgerMenu) {
        hamburgerMenu.addEventListener('click', function() {
            navLinksContainer.classList.toggle('show');
            hamburgerMenu.classList.toggle('active');
            
            // Prevent scrolling when menu is open
            document.body.classList.toggle('menu-open');
            
            // Animate menu items
            const menuItems = document.querySelectorAll('.nav-links li');
            menuItems.forEach((item, index) => {
                if (navLinksContainer.classList.contains('show')) {
                    item.style.animation = `fadeInDown 0.5s ease forwards ${index * 0.1 + 0.2}s`;
                    item.style.opacity = '0';
                } else {
                    item.style.animation = 'none';
                    item.style.opacity = '1';
                }
            });
        });
    }
    
    // Close menu when clicking on a link
    const mobileNavLinks = document.querySelectorAll('.nav-links a');
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navLinksContainer.classList.contains('show')) {
                navLinksContainer.classList.remove('show');
                hamburgerMenu.classList.remove('active');
                document.body.classList.remove('menu-open');
            }
        });
    });
    
    // Animate progress bars on scroll
    const progressBars = document.querySelectorAll('.progress-bar');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const width = entry.target.style.width;
                entry.target.style.width = '0';
                
                setTimeout(() => {
                    entry.target.style.width = width;
                }, 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });
    
    progressBars.forEach(bar => {
        observer.observe(bar);
    });
    
    // Animate chart bars on scroll
    const chartBars = document.querySelectorAll('.bar');
    const chartObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const width = entry.target.style.width;
                entry.target.style.width = '0';
                
                setTimeout(() => {
                    entry.target.style.width = width;
                }, 100);
                
                chartObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });
    
    chartBars.forEach(bar => {
        chartObserver.observe(bar);
    });
    
    // Create placeholder for SVG image
    const createPlaceholderSVG = () => {
        const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.setAttribute("width", "100%");
        svg.setAttribute("height", "400");
        svg.setAttribute("viewBox", "0 0 800 400");
        svg.style.backgroundColor = "#f5f7fa";
        svg.style.borderRadius = "12px";
        
        // Timeline
        const timeline = document.createElementNS("http://www.w3.org/2000/svg", "line");
        timeline.setAttribute("x1", "50");
        timeline.setAttribute("y1", "50");
        timeline.setAttribute("x2", "750");
        timeline.setAttribute("y2", "50");
        timeline.setAttribute("stroke", "#4a7cff");
        timeline.setAttribute("stroke-width", "4");
        svg.appendChild(timeline);
        
        // Years
        const years = [2025, 2026, 2027, 2028, 2029, 2030];
        years.forEach((year, index) => {
            const x = 50 + (700 / 5) * index;
            
            // Year marker
            const marker = document.createElementNS("http://www.w3.org/2000/svg", "circle");
            marker.setAttribute("cx", x);
            marker.setAttribute("cy", "50");
            marker.setAttribute("r", "8");
            marker.setAttribute("fill", "#4a7cff");
            svg.appendChild(marker);
            
            // Year text
            const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
            text.setAttribute("x", x);
            text.setAttribute("y", "80");
            text.setAttribute("text-anchor", "middle");
            text.setAttribute("fill", "#2c3437");
            text.setAttribute("font-weight", "bold");
            text.textContent = year;
            svg.appendChild(text);
            
            // Development path
            if (index < years.length - 1) {
                const contentHeight = 250;
                const contentY = 100;
                
                // Topic
                const topic = document.createElementNS("http://www.w3.org/2000/svg", "text");
                topic.setAttribute("x", x + 15);
                topic.setAttribute("y", contentY + 20 + (index * 40));
                topic.setAttribute("fill", "#2c3437");
                topic.setAttribute("font-weight", "bold");
                
                const topics = ["Large Language Models", "Multimodal Systems", "AI Agents", "Scientific AI", "Creative AI"];
                topic.textContent = topics[index];
                svg.appendChild(topic);
                
                // Progress bar background
                const barBg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
                barBg.setAttribute("x", x + 15);
                barBg.setAttribute("y", contentY + 30 + (index * 40));
                barBg.setAttribute("width", "335");
                barBg.setAttribute("height", "10");
                barBg.setAttribute("rx", "5");
                barBg.setAttribute("fill", "#e1e5ea");
                svg.appendChild(barBg);
                
                // Progress bar
                const progressWidths = [335, 300, 250, 200, 150];
                const bar = document.createElementNS("http://www.w3.org/2000/svg", "rect");
                bar.setAttribute("x", x + 15);
                bar.setAttribute("y", contentY + 30 + (index * 40));
                bar.setAttribute("width", progressWidths[index]);
                bar.setAttribute("height", "10");
                bar.setAttribute("rx", "5");
                bar.setAttribute("fill", "url(#gradient)");
                svg.appendChild(bar);
            }
        });
        
        // Gradient definition
        const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
        const gradient = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
        gradient.setAttribute("id", "gradient");
        gradient.setAttribute("x1", "0%");
        gradient.setAttribute("y1", "0%");
        gradient.setAttribute("x2", "100%");
        gradient.setAttribute("y2", "0%");
        
        const stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
        stop1.setAttribute("offset", "0%");
        stop1.setAttribute("stop-color", "#4a7cff");
        
        const stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
        stop2.setAttribute("offset", "100%");
        stop2.setAttribute("stop-color", "#3d62cc");
        
        gradient.appendChild(stop1);
        gradient.appendChild(stop2);
        defs.appendChild(gradient);
        svg.appendChild(defs);
        
        // Title
        const title = document.createElementNS("http://www.w3.org/2000/svg", "text");
        title.setAttribute("x", "400");
        title.setAttribute("y", "25");
        title.setAttribute("text-anchor", "middle");
        title.setAttribute("fill", "#2c3437");
        title.setAttribute("font-weight", "bold");
        title.setAttribute("font-size", "18");
        title.textContent = "AI Capability Development Timeline";
        svg.appendChild(title);
        
        return svg;
    };
    
    // Add SVG to the page
    const infographicContainer = document.querySelector('.infographic');
    if (infographicContainer) {
        // Create images directory
        const createImagesDir = async () => {
            try {
                // Check if directory exists first
                const checkDir = await fetch('/images', { method: 'HEAD' });
                if (checkDir.status === 404) {
                    const svg = createPlaceholderSVG();
                    const svgString = new XMLSerializer().serializeToString(svg);
                    infographicContainer.innerHTML = svgString;
                } else {
                    // Directory exists, do nothing
                }
            } catch (e) {
                // If error, just insert the SVG directly
                const svg = createPlaceholderSVG();
                const svgString = new XMLSerializer().serializeToString(svg);
                infographicContainer.innerHTML = svgString;
            }
        };
        
        createImagesDir();
    }

    // Render Workforce Impact Chart if the container exists
    const workforceChartContainer = document.getElementById('workforceImpactChart');
    if (workforceChartContainer) {
        renderWorkforceImpactChart();
    }

    // Render Mean Opinion Scores Chart if the container exists
    const meanScoresChartContainer = document.getElementById('meanOpinionScoresChart');
    if (meanScoresChartContainer) {
        renderMeanOpinionScoresChart();
    }

    // Render Binary Results Heatmap if the container exists
    const binaryResultsContainer = document.getElementById('binaryResultsHeatmap');
    if (binaryResultsContainer) {
        renderBinaryResultsHeatmap();
    }

    // Render LLM Evaluation Heatmap if the container exists
    const llmEvaluationContainer = document.getElementById('llmEvaluationHeatmap');
    if (llmEvaluationContainer) {
        renderLlmEvaluationHeatmap();
    }
});

function renderWorkforceImpactChart() {
    const options = {
        series: [{
            name: 'Task Automation Potential',
            data: [95, 85, 80, 75, 70, 65, 60, 55, 45, 30] // Ordered for better visual flow if desired, or match original
        }],
        chart: {
            type: 'bar',
            height: 450,
            toolbar: {
                show: false
            },
            foreColor: 'var(--text-secondary)' // Default text color for chart elements
        },
        plotOptions: {
            bar: {
                horizontal: true,
                borderRadius: 4,
                barHeight: '70%', // Adjust for desired thickness
                distributed: true, // Each bar can have a different color
                dataLabels: {
                    position: 'bottom' // Position of data labels on bars
                }
            }
        },
        colors: [ // Vibrant high-tech colors
            '#00FFFF', // Cyan
            '#FF00FF', // Magenta
            '#00FF7F', // Spring Green
            '#FFFF00', // Yellow
            '#775DD0', // Purple
            '#007BFF', // Blue
            '#FF7F50', // Coral
            '#FFD700', // Gold
            '#ADFF2F', // GreenYellow
            '#FF69B4'  // HotPink
        ],
        dataLabels: {
            enabled: true,
            textAnchor: 'start',
            style: {
                colors: ['#121212'], // Dark text for visibility on bright bars
                fontSize: '12px',
                fontWeight: 'bold'
            },
            formatter: function(val, opt) {
                // Use series name (category) and value
                return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val + "%";
            },
            offsetX: 0,
            dropShadow: {
                enabled: true,
                top: 1,
                left: 1,
                blur: 1,
                opacity: 0.45
            }
        },
        xaxis: {
            categories: [
                'Data Processing', 
                'Basic Content Creation', 
                'Administrative Tasks',
                'Customer Service', 
                'Programming', 
                'Financial Analysis', 
                'Medical Diagnosis', 
                'Education & Training', 
                'Creative Direction', 
                'Physical Caregiving'
            ],
            labels: {
                style: {
                    colors: 'var(--text-secondary)',
                    fontSize: '13px'
                }
            },
            axisBorder: {
                show: true,
                color: 'var(--border-primary)'
            },
            axisTicks: {
                show: true,
                color: 'var(--border-primary)'
            }
        },
        yaxis: {
            labels: {
                show: false // Hide y-axis labels as they are in dataLabels
            }
        },
        grid: {
            borderColor: 'var(--border-primary)',
            strokeDashArray: 4,
            xaxis: {
                lines: {
                    show: true 
                }
            },
            yaxis: {
                lines: {
                    show: false
                }
            }
        },
        tooltip: {
            theme: 'dark', // Use ApexCharts dark theme for tooltip
            y: {
                formatter: function(val) {
                    return val + "%";
                },
                title: {
                    formatter: function (seriesName, opt) {
                        return opt.w.globals.labels[opt.dataPointIndex] || seriesName;
                    }
                }
            }
        },
        stroke: { // Border around bars
            show: true,
            width: 1,
            colors: ['var(--background-primary)']
        },
        legend: {
            show: false // Distributed colors make legend redundant
        }
    };

    const chart = new ApexCharts(document.querySelector("#workforceImpactChart"), options);
    chart.render();
}

function renderMeanOpinionScoresChart() {
    const options = {
        series: [{
            name: 'Holodeck',
            data: [1.8, 2.1, 1.5] // Effectiveness, Arrangement, Scale
        }, {
            name: 'AgentSGEN (No Collision)',
            data: [3.5, 3.2, 3.0]
        }, {
            name: 'AgentSGEN (Collision)',
            data: [5.2, 4.8, 4.6]
        }],
        chart: {
            type: 'bar',
            height: 380,
            toolbar: {
                show: false
            },
            foreColor: 'var(--text-secondary)'
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '60%',
                endingShape: 'rounded',
                borderRadius: 4,
            }
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        xaxis: {
            categories: ['Effectiveness', 'Arrangement', 'Scale Appropriateness'],
            labels: {
                style: {
                    colors: 'var(--text-secondary)',
                    fontSize: '13px'
                }
            },
            axisBorder: {
                color: 'var(--border-primary)'
            },
            axisTicks: {
                color: 'var(--border-primary)'
            }
        },
        yaxis: {
            title: {
                text: 'Mean Opinion Score (1-7)',
                style: {
                    color: 'var(--text-secondary)',
                    fontWeight: 500
                }
            },
            min: 0,
            max: 7,
            tickAmount: 7,
            labels: {
                style: {
                    colors: 'var(--text-secondary)',
                    fontSize: '12px'
                }
            }
        },
        fill: {
            opacity: 1
        },
        colors: ['#707070', '#FF00FF', '#00FFFF'], // Gray, Magenta, Cyan
        legend: {
            position: 'top',
            horizontalAlign: 'center',
            offsetY: 0,
            labels: {
                colors: 'var(--text-primary)'
            },
            markers: {
                width: 12,
                height: 12,
                radius: 12,
            },
            itemMargin: {
                horizontal: 10,
                vertical: 5
            }
        },
        grid: {
            borderColor: 'var(--border-primary)',
            strokeDashArray: 3,
            xaxis: {
                lines: {
                    show: false
                }
            },
            yaxis: {
                lines: {
                    show: true
                }
            }
        },
        tooltip: {
            theme: 'dark',
            y: {
                formatter: function(val) {
                    return val.toFixed(1);
                }
            }
        }
    };

    const chart = new ApexCharts(document.querySelector("#meanOpinionScoresChart"), options);
    chart.render();
}

function renderBinaryResultsHeatmap() {
    const options = {
        series: [
            {
                name: 'Prefers AgentSGEN (Rater 1)',
                data: [ // Corresponds to Rater 2 Prefers AgentSGEN, Rater 2 Prefers Holodeck
                    { x: 'Prefers AgentSGEN (Rater 2)', y: 30 },
                    { x: 'Prefers Holodeck (Rater 2)', y: 8 }
                ]
            },
            {
                name: 'Prefers Holodeck (Rater 1)',
                data: [
                    { x: 'Prefers AgentSGEN (Rater 2)', y: 9 },
                    { x: 'Prefers Holodeck (Rater 2)', y: 6 }
                ]
            }
        ],
        chart: {
            height: 350,
            type: 'heatmap',
            toolbar: { show: false },
            foreColor: 'var(--text-secondary)'
        },
        plotOptions: {
            heatmap: {
                shadeIntensity: 0.5,
                radius: 0,
                useFillColorAsStroke: true,
                colorScale: {
                    ranges: [
                        { from: 0, to: 10, name: 'low', color: '#00A100' },      // Green for low values (agreement on Holodeck)
                        { from: 11, to: 20, name: 'medium', color: '#128FD9' }, // Blue for medium
                        { from: 21, to: 40, name: 'high', color: '#FFB200' }    // Yellow/Orange for high (agreement on AgentSGEN)
                    ]
                }
            }
        },
        dataLabels: {
            enabled: true,
            style: {
                colors: ['#000000'] // Black text for visibility on heatmap colors
            }
        },
        stroke: {
            width: 1,
            colors: ['var(--background-primary)']
        },
        title: {
            text: 'Human Rater Agreement (Binary Preference)',
            align: 'center',
            style: {
                color: 'var(--text-primary)',
                fontSize: '16px'
            }
        },
        tooltip: {
            theme: 'dark'
        },
        xaxis: {
            type: 'category',
            labels: {
                style: { colors: 'var(--text-secondary)'}
            },
             axisBorder: { color: 'var(--border-primary)' },
             axisTicks: { color: 'var(--border-primary)' }
        },
        yaxis: {
            labels: {
                style: { colors: 'var(--text-secondary)'}
            }
        },
        legend: {
             labels: { colors: 'var(--text-primary)'}
        }
    };

    const chart = new ApexCharts(document.querySelector("#binaryResultsHeatmap"), options);
    chart.render();
}

function renderLlmEvaluationHeatmap() {
    const options = {
        series: [
             {
                name: 'AgentSGEN (True)', // Assuming rows are "True Label"
                data: [ // Columns are "Predicted Label"
                    { x: 'AgentSGEN (Pred)', y: 40 }, // TP: LLM correctly identifies AgentSGEN as better
                    { x: 'Holodeck (Pred)', y: 2 }  // FN: LLM incorrectly identifies Holodeck when AgentSGEN was better
                ]
            },
            {
                name: 'Holodeck (True)',
                data: [
                    { x: 'AgentSGEN (Pred)', y: 3 },  // FP: LLM incorrectly identifies AgentSGEN when Holodeck was better/comparable
                    { x: 'Holodeck (Pred)', y: 8 }   // TN: LLM correctly identifies Holodeck as not better (or worse)
                ]
            }
        ],
        chart: {
            height: 350,
            type: 'heatmap',
            toolbar: { show: false },
            foreColor: 'var(--text-secondary)'
        },
        plotOptions: {
            heatmap: {
                shadeIntensity: 0.6,
                radius: 2,
                useFillColorAsStroke: false, // Show cell borders
                colorScale: {
                    ranges: [
                        { from: 0, to: 5, name: 'very low', color: '#FF00FF' }, // Magenta for low (errors/disagreements)
                        { from: 6, to: 15, name: 'low', color: '#775DD0' },  // Purple
                        { from: 16, to: 30, name: 'medium', color: '#007BFF' }, // Blue
                        { from: 31, to: 50, name: 'high', color: '#00FFFF' }   // Cyan for high (correct strong preference)
                    ]
                }
            }
        },
        dataLabels: {
            enabled: true,
            style: {
                colors: ['#000000']
            }
        },
        stroke: {
            width: 1,
            colors: ['var(--background-primary)']
        },
        title: {
            text: 'LLM Evaluation (Preference Matrix)',
            align: 'center',
            style: {
                color: 'var(--text-primary)',
                fontSize: '16px'
            }
        },
        tooltip: {
            theme: 'dark'
        },
         xaxis: {
            type: 'category',
            labels: {
                style: { colors: 'var(--text-secondary)'}
            },
             axisBorder: { color: 'var(--border-primary)' },
             axisTicks: { color: 'var(--border-primary)' }
        },
        yaxis: {
            labels: {
                style: { colors: 'var(--text-secondary)'}
            }
        },
        legend: {
             labels: { colors: 'var(--text-primary)'}
        }
    };

    const chart = new ApexCharts(document.querySelector("#llmEvaluationHeatmap"), options);
    chart.render();
}
