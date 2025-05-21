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
    
    // Navigation background change on scroll
    const nav = document.querySelector('nav');
    
    function updateNavBackground() {
        if (window.scrollY > 100) {
            nav.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
            nav.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.08)';
        } else {
            nav.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
            nav.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
        }
    }
    
    window.addEventListener('scroll', updateNavBackground);
    updateNavBackground();
    
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
});