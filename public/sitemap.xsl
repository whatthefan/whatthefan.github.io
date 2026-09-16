<?xml version="1.0" encoding="UTF-8"?>
<!--
  Esto es solo para los ojos. Un sitemap es un archivo XML pensado para
  los buscadores, asi que al abrirlo en el navegador salia el texto
  crudo, sin formato, y parecia una pagina rota.

  Con esta hoja de estilo, el navegador lo pinta como una tabla legible.
  Google no la lee ni le afecta: se salta la linea <?xml-stylesheet?> y
  ve el XML de siempre.
-->
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">

<xsl:output method="html" encoding="UTF-8" indent="yes"/>

<xsl:template match="/">
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<meta name="robots" content="noindex"/>
<title>Mapa del sitio · PLEA5E</title>
<style>
  :root{--fondo:#0A0E16;--txt:#EEF1F6;--txt-2:#A8B0C0;--oro:#E9BC46;--borde:#20293A}
  *{box-sizing:border-box}
  body{margin:0;padding:32px 20px 56px;background:var(--fondo);color:var(--txt);
    font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
  .caja{max-width:860px;margin:0 auto}
  h1{margin:0 0 6px;font-size:1.5rem;letter-spacing:.01em}
  h1 b{color:var(--oro)}
  .nota{margin:0 0 28px;color:var(--txt-2);font-size:.9rem;max-width:62ch}
  table{width:100%;border-collapse:collapse;font-size:.92rem}
  th{text-align:left;font-size:.72rem;letter-spacing:.09em;text-transform:uppercase;
    color:var(--txt-2);font-weight:600;padding:0 12px 8px 0;border-bottom:1px solid var(--borde)}
  td{padding:14px 12px 14px 0;border-bottom:1px solid var(--borde);vertical-align:top}
  a{color:var(--oro);text-decoration:none;word-break:break-all}
  a:hover{text-decoration:underline}
  .imgs{margin:8px 0 0;padding:0;list-style:none}
  .imgs li{font-size:.8rem;color:var(--txt-2);margin-top:3px}
  .imgs a{color:var(--txt-2)}
  .pie{margin-top:26px;font-size:.8rem;color:var(--txt-2)}
</style>
</head>
<body>
<div class="caja">
  <h1>Mapa del sitio de <b>PLEA5E</b></h1>
  <p class="nota">Esta es la lista que lee Google. La tabla es solo para que se
    entienda al abrirla: el archivo que recibe el buscador es el XML de debajo,
    sin tocar.</p>

  <table>
    <tr>
      <th>Dirección</th>
      <th>Último cambio</th>
    </tr>
    <xsl:for-each select="s:urlset/s:url">
    <tr>
      <td>
        <a href="{s:loc}"><xsl:value-of select="s:loc"/></a>
        <xsl:if test="image:image">
          <ul class="imgs">
          <xsl:for-each select="image:image">
            <li><a href="{image:loc}"><xsl:value-of select="image:loc"/></a></li>
          </xsl:for-each>
          </ul>
        </xsl:if>
      </td>
      <td><xsl:value-of select="s:lastmod"/></td>
    </tr>
    </xsl:for-each>
  </table>

  <p class="pie">
    <xsl:value-of select="count(s:urlset/s:url)"/>
    <xsl:text> dirección(es) · </xsl:text>
    <xsl:value-of select="count(s:urlset/s:url/image:image)"/>
    <xsl:text> imagen(es) · </xsl:text>
    <a href="/robots.txt">robots.txt</a>
  </p>
</div>
</body>
</html>
</xsl:template>

</xsl:stylesheet>
