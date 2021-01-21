from ocrflow.forms import ApprovalForm
from ocrflow.handlers import update_reviewrequest_after_RL1_approval, \
    update_reviewrequest_after_RL2_approval

AUTO_ASSIGNMENT = {
    'initial': {
        'form': ApprovalForm,
        'name': 'ReviewerL1 Review',
        'on_completion': [update_reviewrequest_after_RL1_approval],
        'group': 'ReviewerL1',
        #'next_transition': 'RL2_approval',
        'rules': {
            'auto':{
                'active': True,
                'max_docs_per_reviewer': 5,
                'remainaingDocsDistributionRule': 1
            },
            },
            'custom':{
                'active': False,
                'max_docs_per_reviewer': 5,
                'selected_reviewers': [],
                'remainaingDocsDistributionRule': 1
            },
    },
    'RL2_approval': {
        'form': ApprovalForm,
        'name': 'ReviewerL2 Review',
        'on_completion': [update_reviewrequest_after_RL2_approval],
        'group': 'ReviewerL2'
    }
}
