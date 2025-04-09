import { theme } from '../config/theme';

export const commonStyles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: theme.spacing.md,
    [`@media (max-width: ${theme.breakpoints.sm})`]: {
      padding: theme.spacing.sm
    }
  },
  card: {
    backgroundColor: theme.colors.background,
    borderRadius: theme.borderRadius.md,
    boxShadow: theme.shadows.sm,
    padding: theme.spacing.md,
    marginBottom: theme.spacing.md,
    transition: `all ${theme.animation.duration} ${theme.animation.easing}`,
    '&:hover': {
      boxShadow: theme.shadows.md
    }
  },
  button: {
    backgroundColor: theme.colors.primary,
    color: theme.colors.background,
    padding: `${theme.spacing.sm} ${theme.spacing.md}`,
    borderRadius: theme.borderRadius.sm,
    border: 'none',
    cursor: 'pointer',
    fontSize: theme.typography.button.fontSize,
    fontWeight: theme.typography.button.fontWeight,
    textTransform: theme.typography.button.textTransform,
    transition: `all ${theme.animation.duration} ${theme.animation.easing}`,
    '&:hover': {
      backgroundColor: theme.colors.info
    },
    '&:disabled': {
      backgroundColor: theme.colors.text.disabled,
      cursor: 'not-allowed'
    }
  },
  input: {
    width: '100%',
    padding: theme.spacing.sm,
    borderRadius: theme.borderRadius.sm,
    border: `1px solid ${theme.colors.text.disabled}`,
    fontSize: theme.typography.body1.fontSize,
    lineHeight: theme.typography.body1.lineHeight,
    '&:focus': {
      outline: 'none',
      borderColor: theme.colors.primary
    }
  },
  heading: {
    color: theme.colors.text.primary,
    marginBottom: theme.spacing.md,
    fontFamily: theme.typography.fontFamily,
    '&.h1': theme.typography.h1,
    '&.h2': theme.typography.h2,
    '&.h3': theme.typography.h3
  },
  flexContainer: {
    display: 'flex',
    gap: theme.spacing.md,
    [`@media (max-width: ${theme.breakpoints.sm})`]: {
      flexDirection: 'column'
    }
  },
  gridContainer: {
    display: 'grid',
    gap: theme.spacing.md,
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))'
  },
  badge: {
    display: 'inline-block',
    padding: `${theme.spacing.xs} ${theme.spacing.sm}`,
    borderRadius: theme.borderRadius.sm,
    fontSize: theme.typography.body2.fontSize,
    fontWeight: 500,
    '&.primary': {
      backgroundColor: `${theme.colors.primary}20`,
      color: theme.colors.primary
    },
    '&.success': {
      backgroundColor: `${theme.colors.success}20`,
      color: theme.colors.success
    },
    '&.warning': {
      backgroundColor: `${theme.colors.warning}20`,
      color: theme.colors.warning
    },
    '&.error': {
      backgroundColor: `${theme.colors.error}20`,
      color: theme.colors.error
    }
  },
  icon: {
    fontSize: '1.25rem',
    verticalAlign: 'middle',
    marginRight: theme.spacing.xs
  },
  tooltip: {
    position: 'relative',
    '&:hover::after': {
      content: 'attr(data-tooltip)',
      position: 'absolute',
      bottom: '100%',
      left: '50%',
      transform: 'translateX(-50%)',
      padding: theme.spacing.xs,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      color: theme.colors.background,
      borderRadius: theme.borderRadius.sm,
      fontSize: theme.typography.body2.fontSize,
      whiteSpace: 'nowrap'
    }
  }
}; 