let canvas = new fabric.Canvas('c');


function loadSelectedSVG() {
  const selector = document.getElementById('svg-selector');
  const svgPath = selector.value;

  fabric.loadSVGFromURL(svgPath, function (objects, options) {
    const svg = fabric.util.groupSVGElements(objects, options);
    canvas.clear(); 
    canvas.add(svg);
    canvas.centerObject(svg);
    svg.setCoords();
  }, function (error) {
    console.error("Error loading SVG:", error);
  });
}

// Change the color of clicked objects
document.getElementById('color-picker').addEventListener('click', function (e) {
  if (e.target.classList.contains('color-swatch')) {
    const color = e.target.getAttribute('data-color');
    const activeObject = canvas.getActiveObject();

    if (activeObject && activeObject.set) {
      activeObject.set('fill', color);
      canvas.renderAll();
    }
  }
});


function saveImage() {
  const dataURL = canvas.toDataURL({
    format: 'png',
    quality: 1.0,
  });
  const link = document.createElement('a');
  link.href = dataURL;
  link.download = 'colored_image.png';
  link.click();
}