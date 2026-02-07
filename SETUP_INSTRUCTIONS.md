# Setting Environment Variables for Hugging Face Space

To fix the 500 Internal Server Error on the signup endpoint, you need to set the JWT_SECRET environment variable in your Hugging Face Space:

## Steps to set environment variables in Hugging Face Space:

1. Go to your Hugging Face Space: https://huggingface.co/spaces/komal-agentic-ai-developer-hackathon-2/hackathon-2
2. Click on the "Files" tab
3. Look for a file named "app.yaml" or ".env" or similar configuration file
4. If there's a "Files" section in the space settings, you might be able to add environment variables there

OR

1. Go to the space settings
2. Look for "Environment Variables" or "Secrets" section
3. Add a new environment variable:
   - Name: JWT_SECRET
   - Value: A random string of at least 32 characters (e.g., use a password generator to create a secure key)

## Example of a secure JWT secret:
You can generate one using Python:
```python
import secrets
print(secrets.token_urlsafe(32))  # Generates a 32-byte random string
```

## Alternative approach:
If you can't set environment variables directly, you might need to modify the code to have a hardcoded fallback or use a different approach for the JWT secret in the deployed environment.

## Verification:
After setting the environment variable, restart the Space and test the signup endpoint again.