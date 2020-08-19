module.exports = {
  goldenratio: function(width, height){
    const ratio = (width / height).toFixed(3)
    if (ratio === 1.618) {
      return height
    } else {
      return Math.round(width / 1.618)
    }
  }
}