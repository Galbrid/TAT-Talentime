(function () {
  const configuredBaseUrl = window.__TAT_API_BASE_URL__ || '';
  const productionBaseUrl = 'https://api2.galbrid.online';
  const apiBaseUrl = configuredBaseUrl || productionBaseUrl;

  function resolveUrl(input) {
    if (typeof input !== 'string') return input;

    if (input.startsWith('http://') || input.startsWith('https://')) {
      return input;
    }

    if (input.startsWith('/api/')) {
      return `${apiBaseUrl}${input}`;
    }

    return input;
  }

  const originalFetch = window.fetch.bind(window);
  window.fetch = function (input, init) {
    return originalFetch(resolveUrl(input), init);
  };

  window.TAT_API = {
    baseUrl: apiBaseUrl,
    getUrl: (path) => `${apiBaseUrl}${path.startsWith('/') ? path : '/' + path}`,
  };
})();
