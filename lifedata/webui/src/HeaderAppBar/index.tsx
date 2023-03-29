import AppBar from "@material-ui/core/AppBar";
import Button from "@material-ui/core/Button";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import { makeStyles } from "@material-ui/core/styles";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import AccountCircleIcon from "@material-ui/icons/AccountCircle";
import PowerSettingsNewIcon from "@material-ui/icons/PowerSettingsNew";
import React, { useCallback } from "react";
import { BRAND } from "../branding";
import { User } from "../User";
import { StringConfig } from "../ui_strings";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  header: {
    backgroundColor: BRAND.background,
    color: BRAND.primary,
    // height: theme.spacing(10),
  },
  menuButton: {
    color: "white",
  },
  title: {
    flexGrow: 1,
    fontWeight: "bold",
  },
  iconPadding: {
    paddingRight: theme.spacing(0.5),
  },
}));

export default ({
  user,
  uiStringsConfig,
  annotationCount,
  onLogout = () => {},
}: {
  user: User;
  uiStringsConfig: StringConfig;
  annotationCount: React.ReactFragment;
  onLogout: () => void;
}) => {
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);

  const openUserMenu = useCallback((event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  }, []);
  const closeUserMenu = useCallback(() => {
    setAnchorEl(null);
  }, []);
  return (
    <div className={classes.root}>
      <AppBar color="primary" position="static" className={classes.header}>
        <Toolbar>
          <Typography variant="h4" className={classes.title} component="h1">
            {uiStringsConfig.project_title}
          </Typography>
          <div>{annotationCount}</div>
          <Typography variant="overline"></Typography>
          <Button
            aria-controls="user-menu"
            aria-haspopup="true"
            onClick={openUserMenu}
            color="inherit"
            className={classes.menuButton}
          >
            <AccountCircleIcon className={classes.iconPadding} />
            {user.first_name} {user.last_name}
          </Button>
          <Menu
            id="user-menu"
            anchorEl={anchorEl}
            keepMounted
            open={Boolean(anchorEl)}
            onClose={closeUserMenu}
          >
            <MenuItem onClick={() => onLogout()}>
              <PowerSettingsNewIcon className={classes.iconPadding} />
              Logout
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>
    </div>
  );
};
