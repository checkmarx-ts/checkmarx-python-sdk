import time
import threading


class TokenBucket:
    """
    Token bucket algorithm for rate limiting

    Args:
        capacity: Maximum number of tokens the bucket can hold
        refill_rate: Number of tokens added per second
    """

    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill_time = time.time()
        self.lock = threading.RLock()

    def _refill(self):
        """Refill tokens based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_refill_time
        if elapsed > 0:
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill_time = now

    def consume(self, tokens: int = 1, block: bool = True) -> bool:
        """
        Consume tokens from the bucket

        Args:
            tokens: Number of tokens to consume
            block: Whether to block until tokens are available

        Returns:
            True if tokens were consumed, False otherwise (if block=False and not enough tokens)
        """
        while True:
            with self.lock:
                self._refill()

                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True

                if not block:
                    return False

                # Calculate wait time inside the lock, then sleep outside it
                tokens_needed = tokens - self.tokens
                wait_time = tokens_needed / self.refill_rate
                print(
                    f"Rate limiting: waiting {wait_time:.2f} seconds for {tokens_needed} tokens..."
                )

            # Sleep outside the lock so other threads are not blocked
            time.sleep(wait_time)


class RateLimiter:
    """
    Rate limiter for API requests

    Args:
        capacity: Maximum number of tokens the bucket can hold
        refill_rate: Number of tokens added per second
    """

    def __init__(self, capacity: int = 20000, refill_rate: float = 66.67):
        # Default: 20,000 requests per 5 minutes = 66.67 requests per second
        self.token_bucket = TokenBucket(
            capacity=capacity,  # Maximum tokens
            refill_rate=refill_rate,  # Tokens per second
        )

    def acquire(self, requests: int = 1) -> bool:
        """
        Acquire tokens for API requests

        Args:
            requests: Number of requests to acquire tokens for

        Returns:
            True if tokens were acquired
        """
        return self.token_bucket.consume(requests)

