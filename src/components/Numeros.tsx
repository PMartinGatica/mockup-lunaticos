import { useEffect, useRef, useState } from 'preact/hooks'
import { useProgressiveNumber } from '@/hooks/useProgressiveNumber'

export default function Numeros() {
  const ref = useRef<HTMLDivElement>(null)
  const [visible, setVisible] = useState(false)

  const [productos, setProductos] = useProgressiveNumber(0, 1600, 0)
  const [marcas, setMarcas] = useProgressiveNumber(0, 1200, 0)
  const [clientes, setClientes] = useProgressiveNumber(0, 2000, 0)

  useEffect(() => {
    if (visible) {
      setProductos('100')
      setMarcas('15')
      setClientes('500')
    }
  }, [visible])

  useEffect(() => {
    const obs = new IntersectionObserver(([e]) => { if (e.intersectionRatio > 0) setVisible(true) }, { threshold: 0.2 })
    if (ref.current) obs.observe(ref.current)
    return () => { if (ref.current) obs.unobserve(ref.current) }
  }, [])

  return (
    <section class="relative w-full py-14 md:py-20 overflow-hidden border-y border-white/[0.05]">
      <div class="max-w-7xl mx-auto px-6 md:px-12 lg:px-20" ref={ref}>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10 md:gap-6 text-center">

          <div class="flex flex-col items-center gap-2">
            <span class="font-oswald font-700 text-6xl md:text-7xl lg:text-8xl text-white leading-none">
              +<span class="text-primary">{productos}</span>
            </span>
            <span class="text-white/35 font-dm text-xs tracking-widest uppercase">Productos disponibles</span>
          </div>

          <div class="flex flex-col items-center gap-2">
            <span class="font-oswald font-700 text-6xl md:text-7xl lg:text-8xl text-white leading-none">
              <span class="text-primary">{marcas}</span>+
            </span>
            <span class="text-white/35 font-dm text-xs tracking-widest uppercase">Marcas y equipos</span>
          </div>

          <div class="flex flex-col items-center gap-2">
            <span class="font-oswald font-700 text-6xl md:text-7xl lg:text-8xl text-white leading-none">
              +<span class="text-primary">{clientes}</span>
            </span>
            <span class="text-white/35 font-dm text-xs tracking-widest uppercase">Clientes satisfechos</span>
          </div>

        </div>
      </div>
    </section>
  )
}
