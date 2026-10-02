/* Los 6 vídeos de la guía. Cada escena: {tipo, d (segundos), ...}.
   Textos cortos: no hay voz, se tienen que poder leer a la primera. */
window.VIDEOS = {
  v1: { cap: 'Vídeo 1 · Cómo funciona', escenas: [
    { tipo: 'titulo', d: 3.6, n: '01', t1: 'Así funciona', t2: 'tu placa', pose: 'saluda', dice: '¡En 10 segundos!' },
    { tipo: 'movil', d: 4.6, paso: 'Paso 1', txt: 'El cliente <b>acerca el móvil</b> a la placa', pant: 'nfc' },
    { tipo: 'movil', d: 4.2, paso: '¿Su móvil no lee NFC?', txt: 'Que <b>escanee el QR</b> con la cámara', pant: 'qr' },
    { tipo: 'movil', d: 4.0, paso: 'Paso 2', txt: 'Se abre <b>tu ficha de Google</b>, lista para escribir', pant: 'ficha' },
    { tipo: 'movil', d: 4.2, paso: 'Paso 3', txt: 'Pone las <b>estrellas</b>', pant: 'estrellas' },
    { tipo: 'movil', d: 5.0, paso: 'Paso 4', txt: 'Escribe y pulsa <b>Publicar</b>. ¡Hecho!', pant: 'publicar' },
    { tipo: 'lista', d: 5.6, titulo: 'Y lo mejor', si: ['No descarga ninguna app', 'No tiene que buscarte', 'Solo usa su cuenta de Google de siempre'] },
    { tipo: 'cierre', d: 4.2 } ] },

  v2: { cap: 'Vídeo 2 · Cuándo pedirla', escenas: [
    { tipo: 'titulo', d: 3.6, n: '02', t1: 'Cuándo pedir', t2: 'la reseña', pose: 'curiosa', dice: 'El momento lo es todo' },
    { tipo: 'lista', d: 6.4, titulo: 'Buenos momentos', si: ['Al llevar la cuenta o el datáfono', 'Cuando te dicen «¡estaba todo buenísimo!»', 'Al despedir a un cliente de siempre', 'Después de arreglar bien un problema'] },
    { tipo: 'lista', d: 6.4, titulo: 'Mejor no', no: ['Con el local a tope y el cliente esperando', 'Si algo ha salido mal y aún no está arreglado', 'Nada más sentarse', 'Insistiendo: se pide una vez y ya'] },
    { tipo: 'dato', d: 5.2, grande: 'Que la pida quien cobra', txt: 'Es el último que habla con el cliente y tiene la placa al lado.', pose: 'pulgar' },
    { tipo: 'dato', d: 5.0, grande: 'Pídela a todos', txt: 'Les haya ido como les haya ido. Así lo dicen las normas de Google.', pose: 'senala' },
    { tipo: 'cierre', d: 4.2 } ] },

  v3: { cap: 'Vídeo 3 · Qué decir', escenas: [
    { tipo: 'titulo', d: 3.6, n: '03', t1: 'Qué decir', t2: 'al pedirla', pose: 'guino', dice: 'Toma nota…' },
    { tipo: 'frases', d: 8.2, titulo: 'Frases que funcionan', items: [
      { tag: 'Bar', txt: '«¿Todo bien? Si os ha gustado, nos ayuda un montón una reseña. Es acercar el móvil aquí.»' },
      { tag: 'Cafetería', txt: '«Si te ha gustado el café, una reseña nos ayuda mucho. Acerca el móvil aquí, son dos segundos.»' },
      { tag: 'Peluquería', txt: '«¿Te gusta cómo ha quedado? Si nos dejas una reseña, nos ayudas muchísimo.»' } ] },
    { tipo: 'pasos', d: 7.0, titulo: 'Las tres claves', items: [
      ['Pide ayuda', '«Nos ayuda mucho» funciona. «Ponnos 5 estrellas», no.'],
      ['Di lo fácil que es', '«Acercar el móvil», «dos segundos».'],
      ['Señala', 'La placa, el expositor o la tarjeta: que no tenga que buscar.'] ] },
    { tipo: 'dato', d: 4.6, grande: 'Con tus palabras', txt: 'Una frase corta y con una sonrisa. Suena mejor que una aprendida.', pose: 'pulgar' },
    { tipo: 'cierre', d: 4.2 } ] },

  v4: { cap: 'Vídeo 4 · Dónde ponerla', escenas: [
    { tipo: 'titulo', d: 3.6, n: '04', t1: 'Dónde poner', t2: 'cada placa', pose: 'apunta', dice: 'A la vista, siempre' },
    { tipo: 'pasos', d: 7.6, titulo: 'Cada cosa en su sitio', items: [
      ['Placa de mesa', 'En cada mesa, donde se vea al sentarse: junto al servilletero.'],
      ['Expositor de pie', 'En la barra o junto a la caja: justo donde se paga.'],
      ['Tarjeta de mano', 'Con la cuenta o en el delantal. Para terraza y domicilio.'] ] },
    { tipo: 'lista', d: 6.0, titulo: 'Colócala bien', si: ['A la vista, de cara al cliente', 'Al alcance de la mano'], no: ['Tapada por la carta o el servilletero', 'Detrás de la barra, donde no llega'] },
    { tipo: 'dato', d: 4.8, grande: 'Tu equipo, en 5 minutos', txt: 'Enséñales este vídeo y el anterior. Si lo entienden, lo explican mejor.', pose: 'megafono' },
    { tipo: 'cierre', d: 4.2 } ] },

  v5: { cap: 'Vídeo 5 · Cómo contestar', escenas: [
    { tipo: 'titulo', d: 3.6, n: '05', t1: 'Contesta todas.', t2: 'También las malas', pose: 'elegante', dice: 'Con educación' },
    { tipo: 'pasos', d: 8.2, titulo: 'Paso a paso', items: [
      ['Entra en tu ficha', 'Busca tu negocio en Google con tu cuenta, o abre la app de Google Maps.'],
      ['Abre «Reseñas»', 'Ahí ves las nuevas.'],
      ['Toca «Responder»', 'Escribe tu respuesta y pulsa «Publicar».'] ] },
    { tipo: 'frases', d: 7.4, titulo: 'Respuestas de ejemplo', items: [
      { tag: '★★★★★', txt: '«¡Gracias, Laura! Nos alegra que te gustara la tortilla. Te esperamos pronto.»' },
      { tag: '★★', txt: '«Sentimos la espera, Carlos. No es lo normal en casa. Escríbenos y lo hablamos.»' } ] },
    { tipo: 'lista', d: 6.2, titulo: 'Las reglas', si: ['Usa su nombre y algo de lo que cuenta', 'Corta y amable: dos o tres frases', 'En las malas, lleva la charla a privado'], no: ['Contestar en caliente', 'Discutir en público'] },
    { tipo: 'cierre', d: 4.2 } ] },

  v6: { cap: 'Vídeo 6 · Normas de Google', escenas: [
    { tipo: 'titulo', d: 3.6, n: '06', t1: 'Lo que Google', t2: 'no permite', pose: 'lupa', dice: 'Que no te penalicen' },
    { tipo: 'lista', d: 7.4, titulo: 'Nunca', no: ['Dar algo a cambio: descuentos, chupitos, sorteos…', 'Pedirla solo a los contentos o pedir 5 estrellas', 'Escribirlas tú, tu familia o tu equipo', 'Comprar reseñas', 'Dejar una tablet o un móvil del local para escribirlas'] },
    { tipo: 'lista', d: 5.6, titulo: 'Sí puedes', si: ['Pedirla a todos tus clientes', 'Tener placas, QR y tarjetas a la vista', 'Recordarlo con educación, una vez', 'Contestar a todas'] },
    { tipo: 'dato', d: 5.4, grande: '¿Y la placa?', txt: 'Está dentro de las normas: no regala nada ni elige a quién. Solo le ahorra al cliente tener que buscarte.', pose: 'pulgar' },
    { tipo: 'cierre', d: 4.2 } ] }
};
