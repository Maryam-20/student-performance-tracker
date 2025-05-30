from .models import AcademicSession, Term

def current_session_and_term(request):
    """ 
    Logic to get the most recent Academic Session and term
    """
    current_session = None
    current_term = None
    try:
        # Get the most recent academic session and term
        current_session = AcademicSession.objects.latest('start_date')
        current_term = Term.objects.filter(session=current_session).latest('start_date')
    except AcademicSession.DoesNotExist:
        current_session = None
    except Term.DoesNotExist:
        current_term = None

    return {
        'current_session': current_session,
        'current_term': current_term,
    }