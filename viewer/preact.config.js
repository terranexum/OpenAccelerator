const fs = require('fs');

export default function (config, env, helpers) {
    if (env.production) {
        
        // Use a relative path for the base URL so the web application works when
        // hosting through enterprise or public GitHub Pages.
        config.output.publicPath = '';

    }
}
