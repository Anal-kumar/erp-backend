"""
Rate limiting middleware for API endpoints
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Tuple
import asyncio

class RateLimiter:
    """
    Simple in-memory rate limiter
    For production with multiple servers, use Redis
    """
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = asyncio.Lock()
    
    async def is_allowed(self, identifier: str) -> Tuple[bool, int]:
        """
        Check if request is allowed
        
        Args:
            identifier: IP address or user ID
        
        Returns:
            Tuple of (is_allowed, remaining_requests)
        """
        async with self.lock:
            now = datetime.now()
            minute_ago = now - timedelta(minutes=1)
            
            # Clean old requests
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > minute_ago
            ]
            
            # Check limit
            current_requests = len(self.requests[identifier])
            
            if current_requests >= self.requests_per_minute:
                return False, 0
            
            # Add current request
            self.requests[identifier].append(now)
            remaining = self.requests_per_minute - current_requests - 1
            
            return True, remaining


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware
    """
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.limiter = RateLimiter(requests_per_minute)
        
        # Exempt certain paths from rate limiting
        self.exempt_paths = [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
        ]
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for exempt paths
        if any(request.url.path.startswith(path) for path in self.exempt_paths):
            return await call_next(request)
        
        # Get identifier (IP address or user ID from token)
        identifier = request.client.host
        
        # Check if user is authenticated and use user ID instead
        if "authorization" in request.headers:
            # In production, decode token and use user ID
            # For now, use IP
            pass
        
        # Check rate limit
        is_allowed, remaining = await self.limiter.is_allowed(identifier)
        
        if not is_allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Too many requests. Please try again later.",
                    "retry_after": 60
                },
                headers={
                    "X-RateLimit-Limit": str(self.limiter.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "Retry-After": "60"
                }
            )
        
        # Add rate limit headers to response
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.limiter.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response
