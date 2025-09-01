skill_categories = {
    'programming_languages': {
        'python': ['python', 'python3', 'python programming', 'python development', 'py'],
        'java': ['java', 'java programming', 'java development', 'j2ee', 'j2se'],
        'javascript': ['javascript', 'js', 'ecmascript', 'es6', 'es7', 'es8'],
        'typescript': ['typescript', 'ts', 'typed javascript'],
        'c++': ['c++', 'cpp', 'c plus plus', 'cplusplus'],
        'c#': ['c#', 'csharp', 'dotnet', '.net'],
        'go': ['go', 'golang', 'go programming'],
        'rust': ['rust', 'rust programming', 'rustlang'],
        'swift': ['swift', 'swift programming', 'ios development'],
        'kotlin': ['kotlin', 'kotlin programming', 'android development'],
        'php': ['php', 'php programming', 'php development'],
        'ruby': ['ruby', 'ruby programming', 'ruby on rails', 'rails'],
        'scala': ['scala', 'scala programming', 'functional programming'],
        'r': ['r', 'r programming', 'statistical programming'],
        'matlab': ['matlab', 'matlab programming', 'numerical computing']
    },
    'frameworks': {
        'react': ['react', 'reactjs', 'react.js', 'react native', 'frontend'],
        'angular': ['angular', 'angularjs', 'angular.js', 'frontend framework'],
        'vue': ['vue', 'vuejs', 'vue.js', 'frontend framework'],
        'node.js': ['node.js', 'nodejs', 'node', 'express', 'backend'],
        'django': ['django', 'python web framework', 'backend'],
        'flask': ['flask', 'python microframework', 'backend'],
        'spring': ['spring', 'spring boot', 'spring framework', 'java backend'],
        'laravel': ['laravel', 'php framework', 'backend'],
        'rails': ['rails', 'ruby on rails', 'ror', 'backend'],
        'asp.net': ['asp.net', 'aspnet', 'dotnet', '.net framework'],
        'fastapi': ['fastapi', 'python api framework', 'backend'],
        'gin': ['gin', 'go web framework', 'backend'],
        'actix': ['actix', 'rust web framework', 'backend']
    },
    'databases': {
        'mysql': ['mysql', 'sql database', 'relational database'],
        'postgresql': ['postgresql', 'postgres', 'sql database'],
        'mongodb': ['mongodb', 'mongo', 'nosql', 'document database'],
        'redis': ['redis', 'cache', 'key-value store', 'in-memory database'],
        'elasticsearch': ['elasticsearch', 'elastic search', 'search engine'],
        'sqlite': ['sqlite', 'sql database', 'embedded database'],
        'oracle': ['oracle', 'oracle database', 'enterprise database'],
        'sql server': ['sql server', 'microsoft sql', 'mssql'],
        'cassandra': ['cassandra', 'nosql', 'distributed database'],
        'dynamodb': ['dynamodb', 'aws database', 'nosql'],
        'firebase': ['firebase', 'google database', 'nosql']
    },
    'cloud_platforms': {
        'aws': ['aws', 'amazon web services', 'amazon cloud', 'ec2', 's3', 'lambda'],
        'azure': ['azure', 'microsoft azure', 'microsoft cloud', 'azure devops'],
        'gcp': ['gcp', 'google cloud platform', 'google cloud', 'kubernetes engine'],
        'heroku': ['heroku', 'paas', 'platform as a service'],
        'digitalocean': ['digitalocean', 'droplets', 'vps provider'],
        'linode': ['linode', 'vps provider', 'cloud hosting'],
        'vultr': ['vultr', 'vps provider', 'cloud hosting']
    },
    'devops_tools': {
        'docker': ['docker', 'containerization', 'containers', 'dockerfile'],
        'kubernetes': ['kubernetes', 'k8s', 'container orchestration', 'orchestration'],
        'jenkins': ['jenkins', 'ci/cd', 'continuous integration', 'automation'],
        'git': ['git', 'version control', 'source control', 'github', 'gitlab'],
        'terraform': ['terraform', 'infrastructure as code', 'iac', 'provisioning'],
        'ansible': ['ansible', 'configuration management', 'automation'],
        'chef': ['chef', 'configuration management', 'automation'],
        'puppet': ['puppet', 'configuration management', 'automation'],
        'github actions': ['github actions', 'ci/cd', 'github workflows'],
        'gitlab ci': ['gitlab ci', 'ci/cd', 'gitlab pipelines'],
        'circleci': ['circleci', 'ci/cd', 'continuous integration']
    },
    'ml_ai_tools': {
        'tensorflow': ['tensorflow', 'tf', 'machine learning', 'deep learning'],
        'pytorch': ['pytorch', 'machine learning', 'deep learning', 'neural networks'],
        'scikit-learn': ['scikit-learn', 'sklearn', 'machine learning', 'ml'],
        'pandas': ['pandas', 'data manipulation', 'data analysis', 'python'],
        'numpy': ['numpy', 'numerical computing', 'arrays', 'python'],
        'matplotlib': ['matplotlib', 'data visualization', 'plotting', 'charts'],
        'seaborn': ['seaborn', 'data visualization', 'statistical plots'],
        'opencv': ['opencv', 'computer vision', 'image processing'],
        'nltk': ['nltk', 'natural language processing', 'nlp', 'text analysis'],
        'spacy': ['spacy', 'natural language processing', 'nlp', 'text analysis'],
        'keras': ['keras', 'deep learning', 'neural networks', 'machine learning']
    }
}

experience_indicators = {
    'entry': ['entry level', 'entry-level', 'junior', 'graduate', 'intern', '0-2 years', '0-1 years', 'fresh graduate', 'new graduate'],
    'mid': ['mid level', 'mid-level', 'intermediate', '2-5 years', '3-5 years', 'experienced', 'mid-senior'],
    'senior': ['senior', 'lead', 'principal', '5+ years', '7+ years', '10+ years', 'architect', 'staff engineer', 'senior developer']
}

industry_keywords = {
    'fintech': ['fintech', 'financial technology', 'banking', 'payments', 'blockchain', 'cryptocurrency'],
    'healthcare': ['healthcare', 'medical', 'health tech', 'biotechnology', 'pharmaceuticals'],
    'ecommerce': ['ecommerce', 'e-commerce', 'retail', 'shopping', 'marketplace'],
    'saas': ['saas', 'software as a service', 'b2b', 'enterprise software'],
    'gaming': ['gaming', 'game development', 'entertainment', 'video games'],
    'ai_ml': ['artificial intelligence', 'machine learning', 'ai', 'ml', 'data science']
}

SECRET_KEY = 'my-secret-key' 
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

DEBUG = True
PORT = 5000
