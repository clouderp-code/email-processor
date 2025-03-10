from .base_agent import BaseAgent
from typing import Dict, Any
from datetime import datetime, timedelta
from googleapiclient.discovery import build
import pytz

class MeetingResponderAgent(BaseAgent):
    def __init__(self, calendar_credentials):
        super().__init__()
        self.calendar_service = build(
            'calendar',
            'v3',
            credentials=calendar_credentials
        )
        self.timezone = pytz.UTC

    async def process(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Extract meeting requirements
            meeting_info = self._extract_meeting_info(email_data['body'])
            
            # Check calendar availability
            available_slots = await self._get_available_slots(
                meeting_info['duration'],
                meeting_info['preferred_dates']
            )
            
            # Generate response
            response_content = self._generate_meeting_response(
                email_data,
                available_slots
            )
            
            # Create calendar event draft
            event_draft = await self._create_calendar_event_draft(
                meeting_info,
                available_slots[0] if available_slots else None
            )
            
            result = {
                'status': 'success',
                'response': {
                    'content': response_content,
                    'available_slots': available_slots,
                    'event_draft': event_draft,
                    'type': 'MEETING_RESPONSE',
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            await self.log_processing(email_data, result)
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing meeting request: {str(e)}")
            return {'status': 'error', 'error': str(e)}

    def _extract_meeting_info(self, content: str) -> Dict[str, Any]:
        """Extract meeting details from email content"""
        # Implement meeting info extraction logic
        # This could use NLP to extract duration, preferred dates, etc.
        return {
            'duration': 60,  # default 60 minutes
            'preferred_dates': [
                datetime.now() + timedelta(days=i)
                for i in range(1, 6)
            ],
            'participants': [],
            'topic': "Discussion"
        }

    async def _get_available_slots(
        self,
        duration: int,
        preferred_dates: list
    ) -> list:
        """Find available time slots"""
        available_slots = []
        
        for date in preferred_dates:
            # Get calendar events for the day
            events = self.calendar_service.events().list(
                calendarId='primary',
                timeMin=date.isoformat() + 'Z',
                timeMax=(date + timedelta(days=1)).isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            # Find free slots
            busy_times = [
                (
                    datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date'))),
                    datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date')))
                )
                for event in events.get('items', [])
            ]
            
            # Add available slots
            available_slots.extend(
                self._find_free_slots(date, busy_times, duration)
            )
            
        return available_slots[:5]  # Return top 5 available slots

    def _generate_meeting_response(
        self,
        email_data: Dict[str, Any],
        available_slots: list
    ) -> str:
        """Generate meeting response with available slots"""
        slots_text = "\n".join([
            f"- {slot.strftime('%A, %B %d at %I:%M %p')}"
            for slot in available_slots
        ])
        
        return f"""
        Dear {self._extract_name(email_data['sender'])},

        Thank you for your meeting request. I have checked my calendar and I'm available at the following times:

        {slots_text}

        Please let me know which time works best for you, and I'll send a calendar invitation.

        Best regards,
        [Your Name]
        """

    async def _create_calendar_event_draft(
        self,
        meeting_info: Dict[str, Any],
        preferred_slot: datetime = None
    ) -> Dict[str, Any]:
        """Create a draft calendar event"""
        if not preferred_slot:
            return None
            
        event = {
            'summary': meeting_info['topic'],
            'start': {
                'dateTime': preferred_slot.isoformat(),
                'timeZone': self.timezone.zone,
            },
            'end': {
                'dateTime': (preferred_slot + timedelta(minutes=meeting_info['duration'])).isoformat(),
                'timeZone': self.timezone.zone,
            },
            'attendees': meeting_info['participants'],
            'reminders': {
                'useDefault': True
            }
        }
        
        return event 