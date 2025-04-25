document.getElementById('startBtn').onclick = () => {
    const url = document.getElementById('urlInput').value;
    const pages = document.getElementById('pageInput').value;
  
    // Call the Python API using PyWebView
    pywebview.api.start_scraping(url, pages).then(data => {
      console.log(data); // Handle the response here (e.g., show the URLs in the UI)
      alert('Scraping Complete!');
    }).catch(error => {
      console.error("Error:", error);
      alert('Error during scraping');
    });
  };
  