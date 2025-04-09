const canvas = new fabric.Canvas('c');
let selectedColor = 'red';

// 🎨 Color picker
document.querySelectorAll('.color-swatch').forEach(swatch => {
  swatch.addEventListener('click', () => {
    selectedColor = swatch.dataset.color;
  });
});

// 🖱️ Fill color on shape click
canvas.on('mouse:down', function(opt) {
  const target = opt.target;
  if (target && target.fill !== null) {
    target.set('fill', selectedColor);
    canvas.renderAll();
  }
});

window.loadSelectedSVG = function () {
    const fileName = document.getElementById('svg-selector').value;
    const filePath = `assets/${fileName}`;
  
    console.log("Trying to load:", filePath);  // Debug log
  
    // Clear the canvas
    canvas.clear();
  
    // Load SVG and check results
    fabric.loadSVGFromURL(filePath, function(objects, options) {
      if (!objects || objects.length === 0) {
        alert("No shapes found in SVG. Check the file.");
        return;
      }
  
      const obj = fabric.util.groupSVGElements(objects, options);
      obj.scaleToWidth(600);
      obj.set({ left: 100, top: 50 });
      canvas.add(obj);
      canvas.renderAll();
    }, function (error) {
      console.error("Error loading SVG:", error);
      alert("SVG failed to load. Check file path or format.");
    });
  };
  