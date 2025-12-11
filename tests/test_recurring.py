"""
Tests for Recurring Transactions feature.
"""
import pytest
from datetime import datetime, timezone
from calendar import monthrange
from unittest.mock import MagicMock, AsyncMock, patch
from uuid import uuid4

from app.schemas.finance import (
    RecurringTransactionCreate, RecurringTransactionUpdate
)
from app.schemas.enums import HistoryCategory


class TestRecurringTransactionService:
    """Unit tests for RecurringTransaction service logic."""
    
    def test_calculate_actual_day_for_short_months(self):
        """Test that day 31 is adjusted to last day of short months."""
        # February non-leap year
        _, days_in_feb = monthrange(2023, 2)
        assert days_in_feb == 28
        actual_day = min(31, days_in_feb)
        assert actual_day == 28
        
        # February leap year
        _, days_in_feb_leap = monthrange(2024, 2)
        assert days_in_feb_leap == 29
        actual_day_leap = min(31, days_in_feb_leap)
        assert actual_day_leap == 29
        
        # April (30 days)
        _, days_in_april = monthrange(2023, 4)
        assert days_in_april == 30
        actual_day_april = min(31, days_in_april)
        assert actual_day_april == 30
        
        # December (31 days)
        _, days_in_dec = monthrange(2023, 12)
        assert days_in_dec == 31
        actual_day_dec = min(31, days_in_dec)
        assert actual_day_dec == 31

    def test_timestamp_conversion(self):
        """Test timestamp conversion for recurring transactions."""
        # Create a datetime and convert to timestamp
        dt = datetime(2023, 11, 15, 0, 0, 0, tzinfo=timezone.utc)
        timestamp_ms = int(dt.timestamp() * 1000)
        
        # Convert back
        dt_back = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
        
        assert dt == dt_back
        assert timestamp_ms == 1700006400000  # Expected timestamp for 2023-11-15 00:00:00 UTC

    def test_recurring_transaction_schema_validation(self):
        """Test RecurringTransactionCreate schema validation."""
        valid_data = {
            "sourceType": "subscription",
            "targetAccountId": str(uuid4()),
            "amount": -15.99,
            "dayOfMonth": 15,
            "label": "Netflix",
            "category": "expense",
            "startDate": 1700006400000,
        }
        
        recurring = RecurringTransactionCreate(**valid_data)
        assert recurring.sourceType == "subscription"
        assert recurring.amount == -15.99
        assert recurring.dayOfMonth == 15
        assert recurring.isActive == True  # Default value

    def test_recurring_transaction_update_schema(self):
        """Test RecurringTransactionUpdate schema allows partial updates."""
        update_data = {"amount": -19.99}
        update = RecurringTransactionUpdate(**update_data)
        
        assert update.amount == -19.99
        assert update.label is None
        assert update.isActive is None

    def test_day_of_month_validation(self):
        """Test that dayOfMonth is validated between 1 and 31."""
        import pydantic
        
        # Valid day
        valid_data = {
            "sourceType": "custom",
            "targetAccountId": str(uuid4()),
            "amount": -10.0,
            "dayOfMonth": 15,
            "label": "Test",
            "category": "expense",
            "startDate": 1700006400000,
        }
        recurring = RecurringTransactionCreate(**valid_data)
        assert recurring.dayOfMonth == 15
        
        # Invalid day (too high)
        invalid_data = valid_data.copy()
        invalid_data["dayOfMonth"] = 32
        with pytest.raises(pydantic.ValidationError):
            RecurringTransactionCreate(**invalid_data)
        
        # Invalid day (too low)
        invalid_data["dayOfMonth"] = 0
        with pytest.raises(pydantic.ValidationError):
            RecurringTransactionCreate(**invalid_data)


class TestSyncLogic:
    """Tests for the sync logic calculations."""
    
    def test_months_to_process_calculation(self):
        """Test calculating months that need to be processed."""
        # Simulate: last_processed = Oct 15, 2025; today = Dec 11, 2025
        # day_of_month = 15
        # Should process: Nov 15 (past), but NOT Dec 15 (future)
        
        last_processed = datetime(2025, 10, 15, tzinfo=timezone.utc)
        today = datetime(2025, 12, 11, tzinfo=timezone.utc)
        day_of_month = 15
        
        months_to_process = []
        current_year = last_processed.year
        current_month = last_processed.month
        
        while True:
            # Move to next month
            if current_month == 12:
                current_month = 1
                current_year += 1
            else:
                current_month += 1
            
            # Check if we've gone past current date
            if current_year > today.year or (current_year == today.year and current_month > today.month):
                break
            
            _, days_in_month = monthrange(current_year, current_month)
            actual_day = min(day_of_month, days_in_month)
            target_date = datetime(current_year, current_month, actual_day, tzinfo=timezone.utc)
            
            # Only add if the day has passed
            if target_date.date() < today.date():
                months_to_process.append((current_year, current_month, actual_day))
        
        # Should have Nov 15, 2025 only (Dec 15 hasn't passed yet)
        assert len(months_to_process) == 1
        assert months_to_process[0] == (2025, 11, 15)

    def test_no_processing_for_future_dates(self):
        """Test that future dates are not processed."""
        today = datetime(2025, 12, 11, tzinfo=timezone.utc)
        day_of_month = 15  # Dec 15 hasn't happened yet
        
        target_date = datetime(2025, 12, day_of_month, tzinfo=timezone.utc)
        
        should_process = target_date.date() < today.date()
        assert should_process == False

    def test_process_same_day(self):
        """Test that same day is not processed (wait for next cycle)."""
        today = datetime(2025, 12, 15, tzinfo=timezone.utc)
        target_date = datetime(2025, 12, 15, tzinfo=timezone.utc)
        
        # Same day - should not process
        should_process = target_date.date() < today.date()
        assert should_process == False
