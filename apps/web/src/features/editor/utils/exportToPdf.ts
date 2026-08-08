export async function exportToPdf(htmlContent: string, filename: string = "script.pdf") {
  // Use native browser print to avoid html2canvas CSS parsing errors with modern CSS (oklch)
  const iframe = document.createElement('iframe');
  iframe.style.position = 'absolute';
  iframe.style.width = '0px';
  iframe.style.height = '0px';
  iframe.style.border = 'none';
  document.body.appendChild(iframe);

  const doc = iframe.contentWindow?.document;
  if (!doc) return;

  doc.open();
  doc.write(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>${filename}</title>
        <style>
          body {
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            line-height: 1.5;
            color: black;
            padding: 40px;
          }
          /* Basic formatting for Tiptap tags */
          h1, h2 { text-align: center; font-weight: bold; }
          blockquote { font-style: italic; margin-left: 40px; }
          @media print {
            @page { margin: 1in; }
          }
        </style>
      </head>
      <body>
        ${htmlContent}
      </body>
    </html>
  `);
  doc.close();

  // Give the iframe a moment to render before printing
  setTimeout(() => {
    if (document.body.contains(iframe) && iframe.contentWindow) {
      iframe.contentWindow.focus();
      iframe.contentWindow.print();
      // Cleanup after printing dialog closes
      setTimeout(() => document.body.removeChild(iframe), 1000);
    }
  }, 500);
}
