import html2pdf from "html2pdf.js";

export async function exportToPdf(htmlContent: string, filename: string = "script.pdf") {
  // Create a temporary container for the HTML
  const container = document.createElement("div");
  // Apply base styling so the PDF looks like a script/document
  container.innerHTML = `
    <div style="padding: 40px; font-family: 'Times New Roman', serif; font-size: 12pt; line-height: 1.5; color: black;">
      ${htmlContent}
    </div>
  `;

  const opt = {
    margin:       1,
    filename:     filename,
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2 },
    jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
  };

  await html2pdf().set(opt).from(container).save();
}
