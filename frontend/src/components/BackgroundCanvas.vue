<template>
  <div id="canvas"></div>
</template>

<script>
import Two from 'two.js'

export default {
  name: 'BackgroundCanvas',
  mounted () {
    this.params = {
      fitted: true
    }
    this.el = document.getElementById('canvas')
    this.two = new Two(this.params).appendTo(this.el)
    this.updateBackground()
    window.addEventListener('resize', this.updateBackground)
  },
  methods: {
    updateBackground () {
      this.two.clear()

      let rootHeight = document.getElementById('root').clientHeight
      document.getElementById('canvas').style.height = rootHeight + 'px'
      this.two.renderer.setSize(this.two.renderer.width, rootHeight)
      this.rootHeight = rootHeight

      // Draw line groupings for left and right edge of window
      this.drawLineGroup(Math.floor(window.innerWidth * 0.1), Math.floor(window.innerWidth * 0.1))
      this.drawLineGroup(Math.floor(window.innerWidth * 0.9), Math.floor(window.innerWidth * 0.1))
      // this.drawLeftLines()
      // this.drawRightLines()

      // Draw two additional sets of lines if the viewport is large enough
      let breakpoint = getComputedStyle(document.documentElement).getPropertyValue('--breakpoint-lg')
      if (window.innerWidth > parseInt(breakpoint.substring(0, breakpoint.length - 2))) {
        this.drawLineGroup(Math.floor(window.innerWidth * 0.35), Math.floor(window.innerWidth * 0.1))
        this.drawLineGroup(Math.floor(window.innerWidth * 0.65), Math.floor(window.innerWidth * 0.1))
      }

      this.two.update()
    },
    drawLineGroup (center, width) {
      let colors = ['#00B3C3', '#9A0CBB', '#DADADA']
      let opacity = 1.0
      let offset = 0

      let maxLength = this.rootHeight - 300
      let minLength = Math.floor(this.rootHeight / 2)

      for (let i = 0; i < colors.length * 3; i++) {
        let x = center
        if (i !== 0) {
          let max = center + Math.floor(width / 2)
          let min = center - Math.floor(width / 2)
          x = Math.floor(Math.random() * (max - min + 1) + min)
        }

        this.drawLine(
          center + offset,
          Math.floor(Math.random() * (maxLength - minLength + 1) + minLength),
          colors[i % colors.length],
          opacity,
          i % 2 === 0,
          i % 2 === 1
        )

        opacity -= 0.1
        if (i % 4 === 0) {
          offset += 20
        } else if (i % 4 === 2) {
          offset -= 20
        } else {
          offset *= -1
        }
      }
    },
    drawLine (x, length, stroke, opacity, startTop, turnLeft) {
      let turnOffset = Math.floor(window.innerWidth * 0.015)

      let vertices = []
      if (startTop) {
        vertices.push([x, 0])
        vertices.push([x, length])

        if (turnLeft) {
          vertices.push([x - turnOffset, length + turnOffset])
          vertices.push([x - turnOffset - Math.floor(turnOffset / 3), length + turnOffset])
        } else {
          vertices.push([x + turnOffset, length + turnOffset])
          vertices.push([x + turnOffset + Math.floor(turnOffset / 3), length + turnOffset])
        }
      } else {
        vertices.push([x, this.rootHeight])
        vertices.push([x, this.rootHeight - length])

        if (turnLeft) {
          vertices.push([x - turnOffset, this.rootHeight - length - turnOffset])
          vertices.push([x - turnOffset - Math.floor(turnOffset / 3), this.rootHeight - length - turnOffset])
        } else {
          vertices.push([x + turnOffset, this.rootHeight - length - turnOffset])
          vertices.push([x + turnOffset + Math.floor(turnOffset / 3), this.rootHeight - length - turnOffset])
        }
      }

      let lines = []
      let connections = []
      for (let i = 1; i < vertices.length; i++) {
        lines.push(this.two.makeLine(vertices[i - 1][0], vertices[i - 1][1], vertices[i][0], vertices[i][1]))
        connections.push(this.two.makeCircle(vertices[i][0], vertices[i][1], 1.2))
      }

      let lineGroup = this.two.makeGroup(lines)
      lineGroup.linewidth = 3

      lineGroup.add(connections)
      lineGroup.stroke = stroke
      lineGroup.fill = stroke

      let end = this.two.makeCircle(vertices[vertices.length - 1][0], vertices[vertices.length - 1][1], 2)
      end.stroke = '#ffffff'
      end.fill = '#ffffff'

      lineGroup.add(end)
      lineGroup.opacity = opacity
    }
  }
}
</script>

<style scoped>
#canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -10;
  background: black;
}

svg {
  background: black;
}
</style>
