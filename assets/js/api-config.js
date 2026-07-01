(function () {
  const productionBaseUrl = 'https://api2.galbrid.online';
  const configuredBaseUrl = window.__TAT_API_BASE_URL__ || '';
  const isLocalBaseUrl = (value) => {
    if (!value) return true;
    const normalizedValue = value.toLowerCase();
    return normalizedValue.includes('127.0.0.1') || normalizedValue.includes('localhost') || normalizedValue.includes('0.0.0.0');
  };
  const apiBaseUrl = configuredBaseUrl && !isLocalBaseUrl(configuredBaseUrl) ? configuredBaseUrl : productionBaseUrl;

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
