from abac.const import (
    NOT_APPLICABLE, INDETERMINATE, PERMIT, DENY
)
from .expressions import AbstractExpressions


class Rule:
    """ Class describing the basic behavior of the entity "rule" """

    def __init__(self, target, condition, effect=PERMIT,
                 obligation=None, advice=None, description=None):
        self.target = target
        self.condition = condition
        self.effect = effect
        self.obligation = obligation
        self.advice = advice
        self.description = description
        self.error = None
        self.validate_initialization()

    def decision(self):
        try:
            if self.target is None or self.target.decision() is True:
                if self.condition.decision() is True:
                    return self.effect
            return NOT_APPLICABLE
        except Exception as e:
            self.error = e
            return INDETERMINATE

    def validate_initialization(self):
        if self.target and not isinstance(self.target, AbstractExpressions):
            raise TypeError('The target is not AbstractExpressions or bool')
        if not isinstance(self.condition, AbstractExpressions):
            raise TypeError('The decision is not AbstractExpressions')
        if self.effect not in [PERMIT, DENY]:
            raise TypeError('The effect is not PERMIT or DENY')
        if self.obligation is not None and not callable(self.obligation):
            raise TypeError('The obligation is not callable')
        if self.advice is not None and not callable(self.advice):
            raise TypeError('The advice is not callable')
