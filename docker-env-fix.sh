

echo "=== Docker Environment Variable Troubleshooting ==="
echo

if [ -f ./.env ]; then
    echo "✅ .env file found in the root directory"
    
    PERMISSIONS=$(stat -c "%a" ./.env)
    echo "Current .env file permissions: $PERMISSIONS"
    
    if [ "$PERMISSIONS" != "600" ]; then
        echo "⚠️  Fixing .env file permissions for security..."
        chmod 600 ./.env
        echo "✅ .env file permissions updated to 600 (read/write for owner only)"
    fi
    
    echo "Checking .env file syntax..."
    
    SYNTAX_ERROR=false
    while IFS= read -r line || [ -n "$line" ]; do
        if [[ -z "$line" || "$line" =~ ^# ]]; then
            continue
        fi
        
        if ! [[ "$line" =~ ^[A-Za-z0-9_]+=.* ]]; then
            echo "⚠️  Syntax error in line: $line"
            echo "    Lines should follow KEY=VALUE format (no spaces around =)"
            SYNTAX_ERROR=true
        fi
    done < ./.env
    
    if [ "$SYNTAX_ERROR" = false ]; then
        echo "✅ .env file syntax looks good"
    else
        echo "⚠️  Please fix the syntax errors in your .env file"
    fi
    
    echo "Creating a test environment file with just the API keys..."
    grep -E "OPENAI_API_KEY|NEWS_API_KEY|FMP_API_KEY" ./.env > ./.env.test
    
    echo "✅ Created .env.test with just the API keys for testing"
else
    echo "❌ .env file not found in the root directory!"
    echo "Creating a sample .env file..."
    
    cat > ./.env.sample << EOL
OPENAI_API_KEY=your_openai_api_key
NEWS_API_KEY=your_news_api_key
FMP_API_KEY=your_financial_modeling_prep_api_key

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=512
CHUNK_OVERLAP=50

DEFAULT_AGENT_FRAMEWORK=crewai

REACT_APP_API_URL=http://localhost:8000
EOL
    
    echo "✅ Created .env.sample file. Please rename it to .env and add your API keys."
    exit 1
fi

echo
echo "=== Testing Docker Environment Variable Loading ==="

echo "Testing docker-compose environment variable loading..."
docker-compose config | grep -E "OPENAI_API_KEY|NEWS_API_KEY|FMP_API_KEY" > /dev/null

if [ $? -eq 0 ]; then
    echo "✅ docker-compose can read environment variables from .env"
else
    echo "⚠️  docker-compose cannot read environment variables from .env"
    echo "Trying with explicit --env-file flag..."
    
    echo "Testing with explicit --env-file flag..."
    docker-compose --env-file=./.env config | grep -E "OPENAI_API_KEY|NEWS_API_KEY|FMP_API_KEY" > /dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ docker-compose can read environment variables with --env-file flag"
        echo "SOLUTION: Use 'docker-compose --env-file=./.env up' to start your services"
    else
        echo "❌ docker-compose still cannot read environment variables"
        echo "Let's try with environment variables passed directly..."
        
        OPENAI_API_KEY=$(grep OPENAI_API_KEY ./.env | cut -d '=' -f2)
        NEWS_API_KEY=$(grep NEWS_API_KEY ./.env | cut -d '=' -f2)
        FMP_API_KEY=$(grep FMP_API_KEY ./.env | cut -d '=' -f2)
        
        cat > ./docker-compose-with-env.sh << EOL
export OPENAI_API_KEY="$OPENAI_API_KEY"
export NEWS_API_KEY="$NEWS_API_KEY"
export FMP_API_KEY="$FMP_API_KEY"

echo "Starting docker-compose with environment variables..."
docker-compose \$@
EOL
        
        chmod +x ./docker-compose-with-env.sh
        
        echo "✅ Created docker-compose-with-env.sh wrapper script"
        echo "SOLUTION: Use './docker-compose-with-env.sh up' to start your services"
    fi
fi

echo
echo "=== Recommendations ==="
echo "1. Make sure your .env file is in the root directory of your project"
echo "2. Ensure there are no spaces around the = sign in your .env file"
echo "3. Try using 'docker-compose --env-file=./.env up' to explicitly specify the env file"
echo "4. If all else fails, use the generated wrapper script: './docker-compose-with-env.sh up'"
echo
echo "For more information, see: https://docs.docker.com/compose/environment-variables/"
