"""
ISO 27001 Dashboard - Serenity Pentest  
Modern Streamlit Application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="ISO 27001 Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    return {
  "app": {
    "name": {
      "fr": "Certification ISO 27001 – Serenity Pentest",
      "en": "ISO 27001 Certification – Serenity Pentest"
    },
    "version": "1.4",
    "created_at": "2025-11-11",
    "default_language": "fr",
    "languages": [
      "fr",
      "en"
    ]
  },
  "ui": {
    "views": [
      {
        "id": "view_kanban_status",
        "type": "kanban",
        "group_by": "status",
        "title": {
          "fr": "Suivi par statut",
          "en": "Status tracking"
        }
      },
      {
        "id": "view_table_all",
        "type": "table",
        "columns": [
          "title",
          "owner_person",
          "iso_refs",
          "due_date",
          "status",
          "rag"
        ],
        "title": {
          "fr": "Toutes les tâches",
          "en": "All tasks"
        }
      },
      {
        "id": "view_print_overview",
        "type": "report",
        "template_ref": "report_overview_v1",
        "title": {
          "fr": "Aperçu imprimable",
          "en": "Printable overview"
        }
      },
      {
        "id": "view_timeline",
        "type": "timeline",
        "group_by": "category",
        "title": {
          "fr": "Chronologie du projet",
          "en": "Project timeline"
        },
        "start_field": "created_at",
        "end_field": "due_date",
        "status_field": "status"
      },
      {
        "id": "view_timeline_by_owner",
        "type": "timeline",
        "group_by": "owner_person",
        "title": {
          "fr": "Chronologie par responsable",
          "en": "Timeline by owner"
        },
        "start_field": "created_at",
        "end_field": "due_date",
        "status_field": "status"
      }
    ],
    "status_labels": {
      "done": {
        "fr": "Fait",
        "en": "Done",
        "color": "#16a34a"
      },
      "in_progress": {
        "fr": "En cours",
        "en": "In progress",
        "color": "#f59e0b"
      },
      "not_started": {
        "fr": "Pas encore traité",
        "en": "Not started",
        "color": "#9ca3af"
      }
    },
    "rag_legend": {
      "red": {
        "fr": "En retard / urgent",
        "en": "Overdue / urgent"
      },
      "amber": {
        "fr": "À surveiller",
        "en": "Watch"
      },
      "green": {
        "fr": "OK",
        "en": "OK"
      }
    },
    "forms": {
      "task_status_update": {
        "title": {
          "fr": "Mettre à jour le statut de la tâche",
          "en": "Update task status"
        },
        "entity": "tasks",
        "fields": [
          {
            "name": "id",
            "type": "select",
            "source": "tasks",
            "label": {
              "fr": "Tâche",
              "en": "Task"
            }
          },
          {
            "name": "status",
            "type": "select",
            "options": [
              {
                "value": "done",
                "label": {
                  "fr": "Fait",
                  "en": "Done"
                }
              },
              {
                "value": "in_progress",
                "label": {
                  "fr": "En cours",
                  "en": "In progress"
                }
              },
              {
                "value": "not_started",
                "label": {
                  "fr": "Pas encore traité",
                  "en": "Not started"
                }
              }
            ],
            "label": {
              "fr": "Statut",
              "en": "Status"
            }
          },
          {
            "name": "due_date",
            "type": "date",
            "label": {
              "fr": "Échéance",
              "en": "Due date"
            }
          },
          {
            "name": "next_steps.fr",
            "type": "textarea",
            "label": {
              "fr": "Prochaines étapes (FR)",
              "en": "Next steps (FR)"
            }
          },
          {
            "name": "next_steps.en",
            "type": "textarea",
            "label": {
              "fr": "Next steps (EN)",
              "en": "Next steps (EN)"
            }
          },
          {
            "name": "evidence",
            "type": "list",
            "item_schema": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "file",
                    "url"
                  ]
                },
                "description": {
                  "type": "string"
                },
                "path": {
                  "type": "string"
                }
              }
            },
            "label": {
              "fr": "Preuves (fichiers/liens)",
              "en": "Evidence (files/links)"
            }
          }
        ],
        "permission_required": "tasks:update"
      },
      "stakeholder_add": {
        "title": {
          "fr": "Ajouter une partie prenante",
          "en": "Add stakeholder"
        },
        "entity": "people",
        "fields": [
          {
            "name": "name",
            "type": "text",
            "label": {
              "fr": "Nom complet",
              "en": "Full name"
            }
          },
          {
            "name": "role",
            "type": "text",
            "label": {
              "fr": "Rôle",
              "en": "Role"
            }
          },
          {
            "name": "email",
            "type": "text",
            "label": {
              "fr": "E-mail",
              "en": "Email"
            }
          },
          {
            "name": "phone",
            "type": "text",
            "label": {
              "fr": "Téléphone",
              "en": "Phone"
            }
          }
        ],
        "permission_required": "people:create"
      }
    },
    "actions": {
      "open_task_status_form": {
        "type": "open_form",
        "form_ref": "task_status_update",
        "label": {
          "fr": "Changer le statut d’une tâche",
          "en": "Change task status"
        },
        "visible_for_roles": [
          "admin",
          "manager",
          "contributor"
        ]
      },
      "open_stakeholder_add_form": {
        "type": "open_form",
        "form_ref": "stakeholder_add",
        "label": {
          "fr": "Ajouter une partie prenante",
          "en": "Add stakeholder"
        },
        "visible_for_roles": [
          "admin",
          "manager"
        ]
      },
      "export_pdf_overview": {
        "type": "export_pdf",
        "report_template_ref": "report_overview_v1",
        "default_language": "fr",
        "filename_pattern": "Serenity_ISO27001_Overview_{YYYY}-{MM}-{DD}.pdf",
        "page": {
          "size": "A4",
          "orientation": "portrait",
          "margins": "12mm"
        },
        "title": {
          "fr": "Exporter l’aperçu en PDF",
          "en": "Export Overview to PDF"
        }
      }
    },
    "behaviors": {
      "auto_check": {
        "target": [
          "tasks.status",
          "soa.statement_of_applicability.status"
        ],
        "rule": {
          "if": {
            "status_equals": "done"
          },
          "then": {
            "set": {
              "check": {
                "fr": "Coché",
                "en": "Checked"
              }
            }
          },
          "else": {
            "set": {
              "check": {
                "fr": "Non coché",
                "en": "Unchecked"
              }
            }
          }
        },
        "title": {
          "fr": "Case à cocher automatique",
          "en": "Auto-validation checkbox"
        }
      },
      "overdue_alert": {
        "target": [
          "tasks",
          "soa.statement_of_applicability"
        ],
        "rule": {
          "if": {
            "and": [
              {
                "field_exists": "due_date"
              },
              {
                "date_before_today": "due_date"
              },
              {
                "status_not_equals": "done"
              }
            ]
          },
          "then": {
            "set": {
              "rag": "red",
              "alert": true
            },
            "notify": {
              "level": "warning",
              "message": {
                "fr": "Échéance dépassée : mettre à jour le statut ou la date.",
                "en": "Due date passed: update status or date."
              }
            }
          }
        },
        "title": {
          "fr": "Alerte automatique de retard",
          "en": "Automatic overdue alert"
        }
      }
    }
  },
  "tasks": [
    {
      "id": "T_SOA",
      "title": {
        "fr": "Statement of Applicability (SoA) – 93 contrôles",
        "en": "Statement of Applicability (SoA) – 93 controls"
      },
      "iso_refs": [
        "6.1.3",
        "Annexe A"
      ],
      "category": "Core",
      "owner_person": "Jean-Jacques Kohler",
      "created_at": "2025-11-11",
      "due_date": null,
      "status": "in_progress",
      "rag": "amber",
      "check": {
        "fr": "Non coché",
        "en": "Unchecked"
      },
      "next_steps": {
        "fr": "",
        "en": ""
      },
      "notes": {
        "fr": "",
        "en": ""
      },
      "evidence": []
    },
    {
      "id": "T_POLICY",
      "title": {
        "fr": "PSSI – Validation direction + diffusion",
        "en": "Security Policy – management approval + rollout"
      },
      "iso_refs": [
        "5.1",
        "5.2",
        "7.3"
      ],
      "category": "Core",
      "owner_person": "Marco Generoso",
      "created_at": "2025-11-11",
      "due_date": null,
      "status": "in_progress",
      "rag": "amber",
      "check": {
        "fr": "Non coché",
        "en": "Unchecked"
      },
      "next_steps": {
        "fr": "",
        "en": ""
      },
      "notes": {
        "fr": "",
        "en": ""
      },
      "evidence": []
    },
    {
      "id": "T_INCIDENT",
      "title": {
        "fr": "Processus de gestion des incidents",
        "en": "Incident management process"
      },
      "iso_refs": [
        "A.5.24",
        "A.5.25",
        "A.5.26",
        "A.5.27"
      ],
      "category": "Core",
      "owner_person": "Raphaël",
      "created_at": "2025-11-11",
      "due_date": null,
      "status": "not_started",
      "rag": "amber",
      "check": {
        "fr": "Non coché",
        "en": "Unchecked"
      },
      "next_steps": {
        "fr": "",
        "en": ""
      },
      "notes": {
        "fr": "",
        "en": ""
      },
      "evidence": []
    },
    {
      "id": "T_BCP",
      "title": {
        "fr": "Continuité d’activité (BCP/DRP) – Serenity Pentest",
        "en": "Business Continuity (BCP/DRP) – Serenity Pentest"
      },
      "iso_refs": [
        "A.5.29",
        "A.5.30"
      ],
      "category": "Core",
      "owner_person": "Rémi",
      "created_at": "2025-11-11",
      "due_date": null,
      "status": "not_started",
      "rag": "amber",
      "check": {
        "fr": "Non coché",
        "en": "Unchecked"
      },
      "next_steps": {
        "fr": "",
        "en": ""
      },
      "notes": {
        "fr": "",
        "en": ""
      },
      "evidence": []
    },
    {
      "id": "T_SUPPLIERS",
      "title": {
        "fr": "Gestion des tiers – Horizon3.ai",
        "en": "Third-party management – Horizon3.ai"
      },
      "iso_refs": [
        "A.5.19",
        "A.5.20",
        "A.5.21",
        "A.5.22",
        "A.5.23"
      ],
      "category": "Core",
      "owner_person": "Raphaël",
      "created_at": "2025-11-11",
      "due_date": null,
      "status": "not_started",
      "rag": "amber",
      "check": {
        "fr": "Non coché",
        "en": "Unchecked"
      },
      "next_steps": {
        "fr": "",
        "en": ""
      },
      "notes": {
        "fr": "",
        "en": ""
      },
      "evidence": []
    },
    {
      "id": "T_ACCESS",
      "title": {
        "fr": "Gestion des accès (MFA, revues, offboarding)",
        "en": "Access management (MFA, reviews, offboarding)"
      },
      "iso_refs": [
        "A.5.15",
        "A.5.16",
        "A.5.17",
        "A.5.18"
      ],
      "category": "Core",
      "owner_person": "Raphaël",
      "created_at": "2025-11-11",
      "due_date": null,
      "status": "in_progress",
      "rag": "amber",
      "check": {
        "fr": "Non coché",
        "en": "Unchecked"
      },
      "next_steps": {
        "fr": "",
        "en": ""
      },
      "notes": {
        "fr": "",
        "en": ""
      },
      "evidence": []
    },
    {
      "id": "T_DOCS",
      "title": {
        "fr": "Gestion documentaire (versionning, archivage, suppression)",
        "en": "Document management (versioning, archiving, deletion)"
      },
      "iso_refs": [
        "7.5.1",
        "7.5.2",
        "7.5.3"
      ],
      "category": "Core",
      "owner_person": "Jean-Jacques Kohler",
      "created_at": "2025-11-11",
      "due_date": null,
      "status": "in_progress",
      "rag": "amber",
      "check": {
        "fr": "Non coché",
        "en": "Unchecked"
      },
      "next_steps": {
        "fr": "",
        "en": ""
      },
      "notes": {
        "fr": "",
        "en": ""
      },
      "evidence": []
    },
    {
      "id": "T_LEGAL_PRIVACY",
      "title": {
        "fr": "LPD/RGPD – vidéosurveillance et journaux",
        "en": "LPD/GDPR – CCTV and logs"
      },
      "iso_refs": [
        "A.5.33",
        "A.5.34"
      ],
      "category": "Compliance",
      "owner_person": "Raphaël",
      "created_at": "2025-11-11",
      "due_date": null,
      "status": "in_progress",
      "rag": "amber",
      "check": {
        "fr": "Non coché",
        "en": "Unchecked"
      },
      "next_steps": {
        "fr": "",
        "en": ""
      },
      "notes": {
        "fr": "",
        "en": ""
      },
      "evidence": []
    },
    {
      "id": "T_KPI",
      "title": {
        "fr": "Définir KPI sécurité (mesure efficacité SMSI)",
        "en": "Define security KPIs (ISMS effectiveness)"
      },
      "iso_refs": [
        "9.1"
      ],
      "category": "Governance",
      "owner_person": "Jean-Jacques Kohler",
      "created_at": "2025-11-11",
      "due_date": null,
      "status": "not_started",
      "rag": "amber",
      "check": {
        "fr": "Non coché",
        "en": "Unchecked"
      },
      "next_steps": {
        "fr": "",
        "en": ""
      },
      "notes": {
        "fr": "",
        "en": ""
      },
      "evidence": []
    },
    {
      "id": "T_AUDIT_INT",
      "title": {
        "fr": "Audit interne – plan et exécution",
        "en": "Internal audit – plan and execution"
      },
      "iso_refs": [
        "9.2"
      ],
      "category": "Governance",
      "owner_person": "Jean-Jacques Kohler",
      "created_at": "2025-11-11",
      "due_date": null,
      "status": "not_started",
      "rag": "amber",
      "check": {
        "fr": "Non coché",
        "en": "Unchecked"
      },
      "next_steps": {
        "fr": "",
        "en": ""
      },
      "notes": {
        "fr": "",
        "en": ""
      },
      "evidence": []
    },
    {
      "id": "T_MANAGEMENT_REVIEW",
      "title": {
        "fr": "Revue de direction – préparation",
        "en": "Management review – preparation"
      },
      "iso_refs": [
        "9.3"
      ],
      "category": "Governance",
      "owner_person": "Marco Generoso",
      "created_at": "2025-11-11",
      "due_date": null,
      "status": "not_started",
      "rag": "amber",
      "check": {
        "fr": "Non coché",
        "en": "Unchecked"
      },
      "next_steps": {
        "fr": "",
        "en": ""
      },
      "notes": {
        "fr": "",
        "en": ""
      },
      "evidence": []
    },
    {
      "id": "T_CORRECTIVE",
      "title": {
        "fr": "Non-conformités et actions correctives",
        "en": "Nonconformities and corrective actions"
      },
      "iso_refs": [
        "10.2"
      ],
      "category": "Governance",
      "owner_person": "Jean-Jacques Kohler",
      "created_at": "2025-11-11",
      "due_date": null,
      "status": "not_started",
      "rag": "amber",
      "check": {
        "fr": "Non coché",
        "en": "Unchecked"
      },
      "next_steps": {
        "fr": "",
        "en": ""
      },
      "notes": {
        "fr": "",
        "en": ""
      },
      "evidence": []
    }
  ]
}

# Init
if 'lang' not in st.session_state:
    st.session_state.lang = 'fr'

data = load_data()
lang = st.session_state.lang
tasks = data['tasks']

# Sidebar
with st.sidebar:
    st.title("🛡️ ISO 27001")
    st.markdown("**Serenity Pentest**")
    if st.button("🌐 " + ("EN" if lang == 'fr' else "FR")):
        st.session_state.lang = 'en' if lang == 'fr' else 'fr'
        st.rerun()
    
    st.markdown("---")
    page = st.radio("", ["📊 Overview", "📋 Table", "📈 Charts", "🎯 Kanban"])

# Main title
st.title(data['app']['name'][lang])
st.caption("ISO 27001:2022 Compliance Dashboard")

# Calculate stats
total = len(tasks)
done = sum(1 for t in tasks if t['status'] == 'done')
in_progress = sum(1 for t in tasks if t['status'] == 'in_progress')
not_started = sum(1 for t in tasks if t['status'] == 'not_started')
applicable = sum(1 for t in tasks if t.get('applicable', True))

# Overview page
if "Overview" in page:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Total", total, "ISO 27001:2022")
    col2.metric("✅ Done", done, f"{round(done/total*100,1)}%")
    col3.metric("⏳ In Progress", in_progress)
    col4.metric("⏸️ Not Started", not_started)
    
    st.markdown("---")
    st.subheader("Progress")
    st.progress(done/total)
    st.caption(f"{round(done/total*100,1)}% completed")

# Table page  
elif "Table" in page:
    st.subheader("📋 Controls List")
    
    col1, col2 = st.columns(2)
    with col1:
        search = st.text_input("🔍 Search", placeholder="ID or title...")
    with col2:
        status_filter = st.selectbox("Status", ["All", "done", "in_progress", "not_started"])
    
    # Filter
    filtered = tasks
    if search:
        filtered = [t for t in filtered if search.lower() in t['id'].lower() or search.lower() in t['title'].get(lang, '').lower()]
    if status_filter != "All":
        filtered = [t for t in filtered if t['status'] == status_filter]
    
    # Create DataFrame
    df = pd.DataFrame([{
        'ID': t['id'],
        'Control': t['title'].get(lang, t['title'].get('en', '')),
        'Status': data['ui']['status_labels'][t['status']].get(lang, t['status']),
        'RAG': '🟢' if t.get('rag') == 'green' else '🟡' if t.get('rag') == 'amber' else '🔴',
        'Owner': t.get('owner', 'N/A')
    } for t in filtered])
    
    st.dataframe(df, use_container_width=True, height=600, hide_index=True)
    st.caption(f"{len(filtered)} controls displayed")

# Charts page
elif "Charts" in page:
    st.subheader("📈 Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        status_df = pd.DataFrame({
            'Status': ['Done', 'In Progress', 'Not Started'],
            'Count': [done, in_progress, not_started]
        })
        fig = px.pie(status_df, values='Count', names='Status', title='Status Distribution',
                     color_discrete_sequence=['#10b981', '#f59e0b', '#6b7280'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        rag_green = sum(1 for t in tasks if t.get('rag') == 'green')
        rag_amber = sum(1 for t in tasks if t.get('rag') == 'amber')
        rag_red = sum(1 for t in tasks if t.get('rag') == 'red')
        
        rag_df = pd.DataFrame({
            'RAG': ['Green', 'Amber', 'Red'],
            'Count': [rag_green, rag_amber, rag_red]
        })
        fig2 = px.pie(rag_df, values='Count', names='RAG', title='RAG Distribution',
                      color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444'])
        st.plotly_chart(fig2, use_container_width=True)

# Kanban page
elif "Kanban" in page:
    st.subheader("🎯 Kanban View")
    
    col1, col2, col3 = st.columns(3)
    
    for status, title, col in [
        ('not_started', '⏸️ Not Started', col1),
        ('in_progress', '⏳ In Progress', col2),
        ('done', '✅ Done', col3)
    ]:
        with col:
            status_tasks = [t for t in tasks if t['status'] == status]
            st.markdown(f"### {title}")
            st.caption(f"{len(status_tasks)} controls")
            
            for task in status_tasks:
                rag = '🟢' if task.get('rag') == 'green' else '🟡' if task.get('rag') == 'amber' else '🔴'
                with st.expander(f"{rag} {task['id']}"):
                    st.write(task['title'].get(lang, task['title'].get('en', '')))
                    st.write(f"👤 {task.get('owner', 'N/A')}")

# Footer
st.markdown("---")
st.caption(f"ISO 27001 Dashboard v{data['app']['version']} • {datetime.now().strftime('%Y')}")
