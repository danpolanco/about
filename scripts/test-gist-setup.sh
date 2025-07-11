#!/bin/bash

# Test script to verify gist setup locally
# Usage: ./test-gist-setup.sh <GIST_TOKEN> <GIST_ID>

if [ $# -ne 2 ]; then
    echo "Usage: $0 <GIST_TOKEN> <GIST_ID>"
    echo "Example: $0 ghp_xxxx... e0092caaa6d853193d2a6f69125c13dd"
    exit 1
fi

GIST_TOKEN="$1"
GIST_ID="$2"

echo "🔍 Testing gist setup..."
echo "Gist ID: $GIST_ID"
echo ""

# Test 1: Check if gist exists
echo "📋 Test 1: Check if gist exists"
RESPONSE=$(curl -s -H "Authorization: token $GIST_TOKEN" \
                -H "Accept: application/vnd.github.v3+json" \
                https://api.github.com/gists/$GIST_ID)

if echo "$RESPONSE" | grep -q "\"message\""; then
    echo "❌ Error: $(echo "$RESPONSE" | jq -r .message)"
    echo "Full response: $RESPONSE"
    exit 1
else
    echo "✅ Gist found"
    echo "   Owner: $(echo "$RESPONSE" | jq -r .owner.login)"
    echo "   Public: $(echo "$RESPONSE" | jq -r .public)"
fi

echo ""

# Test 2: Check token permissions
echo "📋 Test 2: Check token permissions"
USER_RESPONSE=$(curl -s -H "Authorization: token $GIST_TOKEN" \
                     -H "Accept: application/vnd.github.v3+json" \
                     https://api.github.com/user)

if echo "$USER_RESPONSE" | grep -q "\"message\""; then
    echo "❌ Token error: $(echo "$USER_RESPONSE" | jq -r .message)"
else
    echo "✅ Token valid"
    echo "   User: $(echo "$USER_RESPONSE" | jq -r .login)"
fi

echo ""

# Test 3: Try to update gist with test content
echo "📋 Test 3: Try updating gist with test content"
TEST_CONTENT='{"test": "This is a test update from local script"}'
ESCAPED_CONTENT=$(echo "$TEST_CONTENT" | jq -Rs .)

UPDATE_RESPONSE=$(curl -s -X PATCH \
                      -H "Authorization: token $GIST_TOKEN" \
                      -H "Accept: application/vnd.github.v3+json" \
                      -d "{\"files\":{\"resume.json\":{\"content\":$ESCAPED_CONTENT}}}" \
                      https://api.github.com/gists/$GIST_ID)

if echo "$UPDATE_RESPONSE" | grep -q "\"message\""; then
    echo "❌ Update failed: $(echo "$UPDATE_RESPONSE" | jq -r .message)"
else
    echo "✅ Update successful"
    echo "   Updated at: $(echo "$UPDATE_RESPONSE" | jq -r .updated_at)"
fi

echo ""
echo "🎯 If all tests pass, your GitHub Actions should work!"
echo "🔗 Check your gist at: https://gist.github.com/$GIST_ID"
