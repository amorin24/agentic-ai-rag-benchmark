
if [ -f ./.env ]; then
    echo "Loading environment variables from .env file..."
    
    while IFS= read -r line || [ -n "$line" ]; do
        if [[ -z "$line" || "$line" =~ ^# ]]; then
            continue
        fi
        
        export "$line"
    done < ./.env
    
    echo "Environment variables loaded successfully!"
else
    echo "Error: .env file not found!"
    echo "Please create a .env file with your API keys."
    exit 1
fi

echo "Starting docker-compose with environment variables..."
docker-compose "$@"
