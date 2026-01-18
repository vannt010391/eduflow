#!/bin/bash

# Eduflow Setup Verification Script
# This script verifies that all components are properly configured

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Eduflow Setup Verification ===${NC}\n"

# Counter for checks
PASSED=0
FAILED=0

# Helper functions
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

check_warn() {
    echo -e "${YELLOW}!${NC} $1"
}

# Check Python
echo -e "${BLUE}Checking Python Installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    check_pass "Python 3 installed: $PYTHON_VERSION"
else
    check_fail "Python 3 not found"
fi

# Check Virtual Environment
echo -e "\n${BLUE}Checking Virtual Environment...${NC}"
if [ -d "venv" ]; then
    check_pass "Virtual environment exists"
    if [ -f "venv/bin/activate" ]; then
        check_pass "Virtual environment is valid"
    else
        check_fail "Virtual environment activation file not found"
    fi
else
    check_warn "Virtual environment not found (run: python3 -m venv venv)"
fi

# Check Required Files
echo -e "\n${BLUE}Checking Required Files...${NC}"
FILES=(
    "manage.py"
    "requirements.txt"
    "eduflow_ai/settings.py"
    "eduflow_ai/wsgi.py"
    ".env.example"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        check_pass "Found: $file"
    else
        check_fail "Missing: $file"
    fi
done

# Check .env Configuration
echo -e "\n${BLUE}Checking Environment Configuration...${NC}"
if [ -f ".env" ]; then
    check_pass ".env file exists"
    
    # Check for SECRET_KEY
    if grep -q "SECRET_KEY" .env; then
        if grep -q "SECRET_KEY=your-secret-key" .env; then
            check_warn ".env: SECRET_KEY is not set (default value)"
        else
            check_pass ".env: SECRET_KEY is configured"
        fi
    else
        check_warn ".env: SECRET_KEY not found"
    fi
    
    # Check for DEBUG setting
    if grep -q "DEBUG" .env; then
        DEBUG_VALUE=$(grep "^DEBUG=" .env | cut -d '=' -f 2)
        check_pass ".env: DEBUG is set to $DEBUG_VALUE"
    else
        check_warn ".env: DEBUG not found"
    fi
else
    check_warn ".env file not found (create from .env.example)"
fi

# Check Database
echo -e "\n${BLUE}Checking Database...${NC}"
if [ -f "db.sqlite3" ]; then
    check_pass "Database file exists: db.sqlite3"
    DB_SIZE=$(ls -lh db.sqlite3 | awk '{print $5}')
    echo "  Database size: $DB_SIZE"
else
    check_warn "Database file not found (run: python manage.py migrate)"
fi

# Check Static Files
echo -e "\n${BLUE}Checking Static Files...${NC}"
if [ -d "staticfiles" ] || [ -d "static" ]; then
    check_pass "Static files directory exists"
else
    check_warn "Static files not collected (run: python manage.py collectstatic)"
fi

# Check Docker
echo -e "\n${BLUE}Checking Docker...${NC}"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    check_pass "Docker installed: $DOCKER_VERSION"
else
    check_warn "Docker not installed"
fi

if command -v docker-compose &> /dev/null; then
    DC_VERSION=$(docker-compose --version)
    check_pass "Docker Compose installed: $DC_VERSION"
else
    check_warn "Docker Compose not installed"
fi

# Check Docker Files
echo -e "\n${BLUE}Checking Docker Configuration...${NC}"
DOCKER_FILES=(
    "Dockerfile"
    "docker-compose.yml"
    "nginx.conf"
    ".dockerignore"
)

for file in "${DOCKER_FILES[@]}"; do
    if [ -f "$file" ]; then
        check_pass "Found: $file"
    else
        check_warn "Missing: $file (Docker deployment won't work)"
    fi
done

# Check Deployment Scripts
echo -e "\n${BLUE}Checking Deployment Scripts...${NC}"
if [ -f "deploy.sh" ]; then
    check_pass "Found: deploy.sh"
    if [ -x "deploy.sh" ]; then
        check_pass "deploy.sh is executable"
    else
        check_warn "deploy.sh is not executable (run: chmod +x deploy.sh)"
    fi
else
    check_warn "Missing: deploy.sh"
fi

# Check CI/CD
echo -e "\n${BLUE}Checking CI/CD Configuration...${NC}"
if [ -f ".github/workflows/tests.yml" ]; then
    check_pass "Found: GitHub Actions tests workflow"
else
    check_warn "Missing: .github/workflows/tests.yml"
fi

if [ -f ".github/workflows/deploy.yml" ]; then
    check_pass "Found: GitHub Actions deploy workflow"
else
    check_warn "Missing: .github/workflows/deploy.yml"
fi

# Check Documentation
echo -e "\n${BLUE}Checking Documentation...${NC}"
DOCS=(
    "README.md"
    "DEPLOYMENT_UBUNTU_24.04.md"
    "DEPLOYMENT_COMPLETE_GUIDE.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        check_pass "Found: $doc"
    else
        check_warn "Missing: $doc"
    fi
done

# Check Git
echo -e "\n${BLUE}Checking Git Configuration...${NC}"
if [ -d ".git" ]; then
    check_pass "Git repository initialized"
    
    REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
    if [ ! -z "$REMOTE" ]; then
        check_pass "Git remote configured: $REMOTE"
    else
        check_warn "Git remote not configured"
    fi
else
    check_warn "Not a Git repository"
fi

# Summary
echo -e "\n${BLUE}=== Verification Summary ===${NC}"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}All checks passed! Your setup is ready.${NC}"
    exit 0
else
    echo -e "\n${YELLOW}Some checks failed. Please review the issues above.${NC}"
    exit 1
fi
