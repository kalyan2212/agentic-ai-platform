"""
Channel-specific migration playbooks
Patent-worthy innovation: Pre-configured migration strategies for different integration types
"""
from typing import List, Dict, Any
from abc import ABC, abstractmethod

from src.models.customer import ChannelType, IntegrationChannel


class MigrationPlaybook(ABC):
    """
    Abstract base class for channel-specific migration playbooks
    
    Patent-worthy innovation: Channel-specific migration strategies that adapt
    to the unique requirements of each integration type
    """
    
    def __init__(self, channel: IntegrationChannel):
        self.channel = channel
        self.steps: List[Dict[str, Any]] = []
    
    @abstractmethod
    def generate_steps(self) -> List[Dict[str, Any]]:
        """Generate migration steps specific to this channel type"""
        pass
    
    def get_prerequisites(self) -> List[str]:
        """Get prerequisites for this migration"""
        return []
    
    def get_validation_checklist(self) -> List[str]:
        """Get validation checklist"""
        return []
    
    def get_rollback_plan(self) -> List[str]:
        """Get rollback plan"""
        return []


class EDIMigrationPlaybook(MigrationPlaybook):
    """
    EDI (Electronic Data Interchange) migration playbook
    Handles X12, EDIFACT, and other EDI standards
    """
    
    def generate_steps(self) -> List[Dict[str, Any]]:
        """Generate EDI-specific migration steps"""
        protocol = self.channel.config.get("protocol", "X12")
        version = self.channel.config.get("version", "unknown")
        
        self.steps = [
            {
                "step_id": "EDI-01",
                "name": "Inventory EDI Documents",
                "description": f"Catalog all {protocol} document types and transaction sets",
                "estimated_duration_hours": 4,
                "automated": True,
                "validation_required": True
            },
            {
                "step_id": "EDI-02",
                "name": "Map EDI Segments",
                "description": f"Map {protocol} segments to modern API data structures",
                "estimated_duration_hours": 16,
                "automated": False,
                "validation_required": True
            },
            {
                "step_id": "EDI-03",
                "name": "Configure Translation Rules",
                "description": "Set up EDI translation and validation rules",
                "estimated_duration_hours": 8,
                "automated": False,
                "validation_required": True
            },
            {
                "step_id": "EDI-04",
                "name": "Test EDI Transactions",
                "description": "Validate sample EDI transactions through new platform",
                "estimated_duration_hours": 12,
                "automated": True,
                "validation_required": True
            },
            {
                "step_id": "EDI-05",
                "name": "Configure Trading Partner",
                "description": "Set up trading partner configuration in new system",
                "estimated_duration_hours": 4,
                "automated": False,
                "validation_required": True
            },
            {
                "step_id": "EDI-06",
                "name": "Parallel Testing",
                "description": "Run parallel EDI processing in both systems",
                "estimated_duration_hours": 40,
                "automated": True,
                "validation_required": True
            },
            {
                "step_id": "EDI-07",
                "name": "Cutover Execution",
                "description": "Switch EDI traffic to new platform",
                "estimated_duration_hours": 2,
                "automated": False,
                "validation_required": True
            }
        ]
        return self.steps
    
    def get_prerequisites(self) -> List[str]:
        return [
            "EDI document specifications and trading partner agreements",
            "Sample EDI files for each transaction type",
            "Legacy EDI gateway configuration",
            "Trading partner contact information",
            "EDI compliance requirements"
        ]
    
    def get_validation_checklist(self) -> List[str]:
        return [
            "All EDI document types mapped correctly",
            "Segment translations validated",
            "Acknowledgments (997/999) working properly",
            "Error handling and logging configured",
            "Trading partner connectivity verified",
            "Compliance rules validated"
        ]
    
    def get_rollback_plan(self) -> List[str]:
        return [
            "Revert trading partner routing to legacy gateway",
            "Disable new EDI endpoint",
            "Restore legacy EDI processing",
            "Notify trading partners of temporary reversion",
            "Analyze failure logs for root cause"
        ]


class SFTPMigrationPlaybook(MigrationPlaybook):
    """SFTP migration playbook"""
    
    def generate_steps(self) -> List[Dict[str, Any]]:
        self.steps = [
            {
                "step_id": "SFTP-01",
                "name": "Inventory File Patterns",
                "description": "Catalog all file patterns, formats, and schedules",
                "estimated_duration_hours": 2,
                "automated": True,
                "validation_required": True
            },
            {
                "step_id": "SFTP-02",
                "name": "Configure New SFTP Server",
                "description": "Set up SFTP server and user accounts",
                "estimated_duration_hours": 4,
                "automated": False,
                "validation_required": True
            },
            {
                "step_id": "SFTP-03",
                "name": "Migrate File Processing Logic",
                "description": "Transfer file parsing and validation logic",
                "estimated_duration_hours": 8,
                "automated": False,
                "validation_required": True
            },
            {
                "step_id": "SFTP-04",
                "name": "Test File Transfers",
                "description": "Validate file upload, download, and processing",
                "estimated_duration_hours": 6,
                "automated": True,
                "validation_required": True
            },
            {
                "step_id": "SFTP-05",
                "name": "Update Client Credentials",
                "description": "Provide new SFTP credentials to customer",
                "estimated_duration_hours": 2,
                "automated": False,
                "validation_required": True
            },
            {
                "step_id": "SFTP-06",
                "name": "Cutover Execution",
                "description": "Switch to new SFTP server",
                "estimated_duration_hours": 1,
                "automated": False,
                "validation_required": True
            }
        ]
        return self.steps
    
    def get_prerequisites(self) -> List[str]:
        return [
            "File format specifications",
            "Sample files for each type",
            "Current SFTP schedules and frequency",
            "Encryption and security requirements",
            "File retention policies"
        ]
    
    def get_validation_checklist(self) -> List[str]:
        return [
            "File uploads successful",
            "File downloads successful",
            "File parsing working correctly",
            "Error notifications configured",
            "Archive and cleanup jobs scheduled",
            "Security and encryption verified"
        ]


class APIRigrationPlaybook(MigrationPlaybook):
    """REST/SOAP API migration playbook"""
    
    def generate_steps(self) -> List[Dict[str, Any]]:
        api_type = self.channel.config.get("api_type", "REST")
        
        self.steps = [
            {
                "step_id": "API-01",
                "name": "API Contract Analysis",
                "description": f"Analyze {api_type} API contracts and endpoints",
                "estimated_duration_hours": 4,
                "automated": True,
                "validation_required": True
            },
            {
                "step_id": "API-02",
                "name": "Map Endpoints",
                "description": "Map legacy endpoints to new API",
                "estimated_duration_hours": 8,
                "automated": False,
                "validation_required": True
            },
            {
                "step_id": "API-03",
                "name": "Implement Adapters",
                "description": "Create compatibility adapters if needed",
                "estimated_duration_hours": 16,
                "automated": False,
                "validation_required": True
            },
            {
                "step_id": "API-04",
                "name": "Test API Calls",
                "description": "Validate all API endpoints with test data",
                "estimated_duration_hours": 12,
                "automated": True,
                "validation_required": True
            },
            {
                "step_id": "API-05",
                "name": "Update API Documentation",
                "description": "Provide updated API documentation to customer",
                "estimated_duration_hours": 4,
                "automated": False,
                "validation_required": True
            },
            {
                "step_id": "API-06",
                "name": "Phased Rollout",
                "description": "Gradually route API traffic to new platform",
                "estimated_duration_hours": 8,
                "automated": True,
                "validation_required": True
            }
        ]
        return self.steps
    
    def get_prerequisites(self) -> List[str]:
        return [
            "API documentation (OpenAPI/Swagger spec)",
            "Authentication mechanism details",
            "Rate limiting and throttling requirements",
            "Sample request/response payloads",
            "Error handling requirements"
        ]
    
    def get_validation_checklist(self) -> List[str]:
        return [
            "All endpoints responding correctly",
            "Authentication working properly",
            "Request/response schemas validated",
            "Error responses consistent",
            "Rate limiting configured",
            "API versioning strategy implemented"
        ]


class ThickClientMigrationPlaybook(MigrationPlaybook):
    """Thick client application migration playbook"""
    
    def generate_steps(self) -> List[Dict[str, Any]]:
        self.steps = [
            {
                "step_id": "CLIENT-01",
                "name": "Application Assessment",
                "description": "Analyze thick client architecture and dependencies",
                "estimated_duration_hours": 8,
                "automated": False,
                "validation_required": True
            },
            {
                "step_id": "CLIENT-02",
                "name": "Develop Web/Cloud Alternative",
                "description": "Build modern web or cloud-native alternative",
                "estimated_duration_hours": 80,
                "automated": False,
                "validation_required": True
            },
            {
                "step_id": "CLIENT-03",
                "name": "Data Migration",
                "description": "Migrate local data to cloud storage",
                "estimated_duration_hours": 16,
                "automated": True,
                "validation_required": True
            },
            {
                "step_id": "CLIENT-04",
                "name": "User Acceptance Testing",
                "description": "Conduct UAT with customer users",
                "estimated_duration_hours": 40,
                "automated": False,
                "validation_required": True
            },
            {
                "step_id": "CLIENT-05",
                "name": "Training",
                "description": "Train customer users on new platform",
                "estimated_duration_hours": 16,
                "automated": False,
                "validation_required": True
            },
            {
                "step_id": "CLIENT-06",
                "name": "Deployment",
                "description": "Deploy new application to customer users",
                "estimated_duration_hours": 8,
                "automated": False,
                "validation_required": True
            }
        ]
        return self.steps
    
    def get_prerequisites(self) -> List[str]:
        return [
            "Thick client application documentation",
            "User workflow documentation",
            "Local data storage locations",
            "Integration points with other systems",
            "User access and permission requirements"
        ]
    
    def get_validation_checklist(self) -> List[str]:
        return [
            "All features functional in new application",
            "Data migrated completely and accurately",
            "User workflows validated",
            "Performance meets requirements",
            "Training materials prepared",
            "Support procedures documented"
        ]


class PlaybookFactory:
    """Factory for creating appropriate playbooks"""
    
    @staticmethod
    def create_playbook(channel: IntegrationChannel) -> MigrationPlaybook:
        """Create appropriate playbook for channel type"""
        playbook_map = {
            ChannelType.EDI: EDIMigrationPlaybook,
            ChannelType.SFTP: SFTPMigrationPlaybook,
            ChannelType.REST_API: APIRigrationPlaybook,
            ChannelType.SOAP_API: APIRigrationPlaybook,
            ChannelType.THICK_CLIENT: ThickClientMigrationPlaybook,
            ChannelType.WEB_PORTAL: APIRigrationPlaybook,  # Treat web portal like API
        }
        
        playbook_class = playbook_map.get(channel.channel_type, MigrationPlaybook)
        return playbook_class(channel)
