"""Enterprise security controls: RBAC, audit, encryption."""

from dataclasses import dataclass, field
from enum import Enum


class Role(str, Enum):
    SOLVER = "solver"
    PLANNER = "planner"
    WORKER = "worker"
    EVALUATOR = "evaluator"
    POLICY_ADMIN = "policy_admin"


class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    APPROVE = "approve"
    AUDIT = "audit"


@dataclass(slots=True)
class AuditLog:
    timestamp: str
    actor: str
    action: str
    resource: str
    status: str
    details: dict = field(default_factory=dict)


class RBAC:
    """Role-Based Access Control."""

    def __init__(self) -> None:
        self.role_permissions: dict[Role, set[Permission]] = {
            Role.SOLVER: {Permission.READ, Permission.EXECUTE},
            Role.PLANNER: {Permission.READ, Permission.EXECUTE},
            Role.WORKER: {Permission.READ, Permission.WRITE, Permission.EXECUTE},
            Role.EVALUATOR: {Permission.READ, Permission.EXECUTE, Permission.AUDIT},
            Role.POLICY_ADMIN: {Permission.READ, Permission.WRITE, Permission.APPROVE, Permission.AUDIT},
        }
        self.audit_trail: list[AuditLog] = []

    def check_permission(self, role: Role, permission: Permission) -> bool:
        """Check if role has permission."""
        return permission in self.role_permissions.get(role, set())

    def log_action(self, audit_event: AuditLog) -> None:
        """Record action in audit trail."""
        self.audit_trail.append(audit_event)
